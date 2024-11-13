from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/like/dream/(?P<id>\d+)/$", consumers.LikeConsumer.as_asgi()),
    re_path(r"ws/like/dream/main_page/$", consumers.MainPageLikeConsumer.as_asgi()),
]