# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game, GameMove
from channels.db import database_sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'move':
            await self.save_move(data['move'])

    @database_sync_to_async
    def save_move(self, move_data):
        GameMove.objects.create(
            game_id=self.game_id,
            player_id=move_data['player_id'],
            move=move_data['move']
        )

    async def game_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GameMove

@receiver(post_save, sender=GameMove)
def broadcast_move(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{instance.game_id}",
            {
                "type": "game_update",
                "message": {
                    "type": "new_move",
                    "move": instance.to_dict()
                }
            }
        )