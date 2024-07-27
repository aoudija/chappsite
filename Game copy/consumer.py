import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Models.models import User
from models import Match
from utils import gameLogic
'''

    movement
    action
    id
    wWidth
    wHeight
    upO , downO
    upP , downP

'''
class gameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"
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

        if action == 'play':
            gc = gameLogic(data)
            await self.channel_layer.group_send(
                self.room_group_name, {
                                    "type": "send_data",
                                    "action":action,
                                    "game_id": gc.id,
                                    "player_y": gc.player_y,
                                    "opponent_y": gc.opponent_y
                                    }
            )
        # if action == 'inviteSent':
        #     await self.channel_layer.group_send(
        #         self.room_group_name, {
        #                             "type": "send_data",
        #                             "action": action,
        #                             "from": data['from'],
        #                             "sendTo": data['sendTo']
        #                             }
        #     )
        # elif action == 'inviteAccept':
        #     player = User.objects.get(username=data['palyer'])
        #     opponent = User.objects.get(username=data['opponent'])
        #     gc = Match.objects.get(id=data['id'])
        #     gc.player = player
        #     gc.opponent = opponent
        #     await self.channel_layer.group_send(
        #         self.room_group_name, {
        #                             "type": "send_data",
        #                             "action": action,
        #                             "from": data['from'],
        #                             "gameId": gc.id,
        #                             }
        #     )
        elif action == 'inviteDeclined':
            await self.channel_layer.group_send(
                self.room_group_name, {
                                    "type": "send_data",
                                    "action": action,
                                    "from": data['from'],
                                    "sendTo": data['sendTo']
                                    }
            )

    async def send_data(self, event):
        await self.send(json.dumps(event))