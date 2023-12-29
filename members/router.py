# chat/routing.py

from django.urls import re_path

from members.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/bin/', ChatConsumer.as_asgi()),
]