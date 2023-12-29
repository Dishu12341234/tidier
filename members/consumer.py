import json

from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import BinsStats as Bin


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.BindID = None
        self.BindIDGroup = None

    def connect(self):
        print("WebSocket connection established")
        
        self.BindID = self.scope
        print("BindID:", self.BindID)
        self.BindID = "A"
        print("BindID:", self.BindID)

        self.BindIDGroup = f'Group_{self.BindID}'
        print("BindIDGroup:", self.BindIDGroup)

        # connection has to be accepted 
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.BindIDGroup,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.BindIDGroup,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.BindIDGroup,
            {
                'type': 'BinReload',
                'Area': f"{text_data}",
            }
        )
    def BinReload(self, event):
        bins_data = list(Bin.objects.values())
        bins_serializable = json.dumps({
            'type': 'BinReload',
            'bins': bins_data,
        }, cls=DjangoJSONEncoder)

        self.send(text_data=bins_serializable)