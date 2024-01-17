from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Statistic, DataItem, ChatRoom, ChatMessage
from DashBoards.backend_funcs import generate_random_color

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f"stats-{dashboard_slug}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f'connection closed with code: {close_code}')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        print(message)
        print(sender)

        dashboard_slug = self.dashboard_slug

        await self.save_data_item(sender, message, dashboard_slug)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'statistics_message',
            'message': message,
            'sender': sender,
        })

    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def create_data_item(self, sender, message, slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(statistic=obj, value=message, owner=sender)

    async def save_data_item(self, sender, message, slug):
        await self.create_data_item(sender, message, slug)


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        name = self.scope['url_route']['kwargs']['name']
        self.name = name
        self.room_group_name = f"room-{name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f'connection closed with code: {close_code}')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_existing_owner(self, sender):
        return ChatMessage.objects.filter(owner=sender).first()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        existing_owner = await self.get_existing_owner(sender)
        if existing_owner:
            color = existing_owner.color
        else:
            color = generate_random_color()

        name = self.name

        await self.save_chat_message(sender, message, color, name)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'sender': sender,
            'color': color,
        })

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        color = event['color']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'color': color
        }))

    @database_sync_to_async
    def create_chat_message(self, sender, message, color, name):
        obj = ChatRoom.objects.get(name=name)
        existing_message = ChatMessage.objects.filter(owner=sender).first()
        if existing_message:
            return ChatMessage.objects.create(room=obj, value=message, owner=sender, color=existing_message.color)
        else:
            return ChatMessage.objects.create(room=obj, value=message, owner=sender, color=color)

    async def save_chat_message(self, sender, message, color, name):
        await self.create_chat_message(sender, message, color, name)