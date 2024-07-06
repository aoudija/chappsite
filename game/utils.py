from models import gameCoordinates
from django.contrib.auth.models import User

def gameLogic(data):
    
    player = User.objects.get(username=data['palyer'])
    opponent = User.objects.get(username=data['opponent'])
    movement = data['movement']

    try:
        gc = gameCoordinates.objects.get(player = player, opponent = opponent)
    except:
        gc = gameCoordinates()
        gc.player = player
        gc.opponent = opponent
    
    if movement == 'up':
        move = 10
    elif movement == 'down' :
        move = -10
    elif movement == 'stop':
        move = 0
    
    gc.py += move
    gc.save()
    return gc
#still needs up down protections
# await sync_to_async(initialize_msg_instance)(text_data_json)
# Send message to room group => show in room