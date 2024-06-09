import json
from channels.generic.websocket import AsyncWebsocketConsumer
from models import gameCoordinates
from django.contrib.auth.models import User

class gameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # self.username = self.scope['user'].username

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        self.accept()
    
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.load(text_data)
        action = data['action']
        player_username = data['palyer']
        opponent_username = data['opponent']

        player = User.objects.get(username=player_username)
        opponent = User.objects.get(username=opponent_username)
        try:
            gc = gameCoordinates.objects.get(player = player, opponent = opponent)
        except:
            gc = gameCoordinates()
            gc.player = player
            gc.opponent = opponent
        if action == 'up':
            move = 10
        elif action == 'down' :
            move = -10
        elif action == 'stop':
            move = 0
        gc.py += move
        gc.save()
        #still needs up down protections
        # await sync_to_async(initialize_msg_instance)(text_data_json)
        # Send message to room group => show in room
        await self.channel_layer.group_send(
            self.room_group_name, {
                                "type": "send_coordinates",
                                "player_made_action": data["player"],
                                "player_y": gc.py
                                }
        )
#nqd nzid .value later for Y
    async def send_coordinates(self, event):
        player_made_action = event['player_made_action']
        player_y = event['player_y']
        await self.send(text_data=json.dumps({
            "player_made_action": player_made_action,
            "player_y": player_y
        }))