import json

from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import BinsStats as time

#Single class for a singlw task
class BinConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = None
        self.BinGroup = None

    def connect(self):
        print("WebSocket connection established")

        self.time = self.scope["url_route"]["kwargs"]["time"]
        print("time:", self.time)

        self.BinGroup = f"Group_{self.time}"
        print("BinGroup:", self.BinGroup)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.BinGroup,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.BinGroup,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        # send chat message event to the room
        print("Text data", end="\n")
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.BinGroup,
            {
                "type": f"{data['type']}",
            },
        )

    def BinReload(self, event):
        bins_data = list(time.objects.values().order_by('-fillUp'))
        bins_serializable = json.dumps(
            {
                "type": event["type"],
                "bins": bins_data,
            },
            cls=DjangoJSONEncoder,
        )

        self.send(text_data=bins_serializable)
