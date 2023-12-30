import json

from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import BinsStats as Bin


class BinConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.Bin = None
        self.BinGroup = None

    def connect(self):
        print("WebSocket connection established")

        self.Bin = "Bin"
        print("Bin:", self.Bin)

        self.BinGroup = f"Group_{self.Bin}"
        print("BinGroup:", self.BinGroup)
        print(self.scope)

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
        print("Text data", end="\n\n\n\n\n\n\n\n\n\n\n")
        async_to_sync(self.channel_layer.group_send)(
            self.BinGroup,
            {
                "type": f"{text_data}",#If the text_data is BinRelaod then call the function with the same type
            },
        )

    def BinReload(self, event):
        bins_data = list(Bin.objects.values())
        bins_serializable = json.dumps(
            {
                "type": "BinReload",#This is the function with the type BinReload so if the recived text_data in the recive function is BinReload then this function would be called
                "bins": bins_data,
            },
            cls=DjangoJSONEncoder,
        )

        self.send(text_data=bins_serializable)
