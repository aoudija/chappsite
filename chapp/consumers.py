import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

def initialize_msg_instance(text_data_json):
    msg = Messages()
    msg.content = text_data_json["message"]
    msg.sender = User.objects.get(username=text_data_json["sender"])
    msg.receiver = User.objects.get(username=text_data_json["receiver"])
    msg.save()

def get_messages(event):
    sender = User.objects.get(username=event["sender"])
    msgs_sent1 = sender.sent_messages.all()
    message_list = []
    for msg in msgs_sent1:
        message_dict = {
            'content': msg.content,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'date_of_message': msg.date_of_message.strftime("%Y-%m-%d %H:%M:%S"),
        }
        message_list.append(message_dict)
    return message_list

def is_authorized(scope):
    user = User.objects.get(username=scope['user'])
    return user.is_authenticated

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not await sync_to_async(is_authorized)(self.scope):
            await self.close(code=4003)

        print(f"\033[33m testing... \033[0m")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await sync_to_async(initialize_msg_instance)(text_data_json)
        # Send message to room group => show in room
        await self.channel_layer.group_send(
            self.room_group_name, {
                                   "type": "chat.message",
                                   "sender": text_data_json["sender"],
                                   "receiver": text_data_json["receiver"],
                                   "message": message
                                   }
        )

    async def chat_message(self, event):
        message_dict = await sync_to_async(get_messages)(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message_dict))
        #json sent ot front
