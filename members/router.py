# chat/routing.py

from django.urls import re_path

from members.consumer import BinConsumer

websocket_urlpatterns = [
    re_path(r'ws/bin/(?P<time>\w+)/$', BinConsumer.as_asgi()),
]