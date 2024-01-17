from django.urls import path
from .consumers import DashboardConsumer, ChatRoomConsumer

websocket_urlpatterns = [
    path('ws/stats/<str:dashboard_slug>/', DashboardConsumer.as_asgi()),
    path('ws/chat/<str:name>/', ChatRoomConsumer.as_asgi()),
]