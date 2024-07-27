from models import Match
from django.contrib.auth.models import User

def gameLogic(data):
    
    player = User.objects.get(username=data['palyer'])
    opponent = User.objects.get(username=data['opponent'])
    movement = data['movement']

    gc = Match.objects.get(
        player = player,
        opponent = opponent,
        id = data['id']
        )
    #-------------ballAnimation-------------
    gc.ball_x += gc.ball_speed_x
    gc.ball_y += gc.ball_speed_y

    #ballRestartForLaterCheck Reminder !!

    #topBottomCheck
    if gc.ball_y - 15 <= 0:
        gc.ball_y = 15
        gc.ball_speed_y *= -1
    elif gc.ball_y + 15 >= data['wHeight']:
        gc.ball_y = data['wHeight'] - 15
        gc.ball_speed_y *= -1


    #scoreCheck
    if gc.ball_x - 15 <= 0:
        gc.scored = True
        gc.scoreOpponent += 1
    if gc.ball_x + 15 >= data['wWidth']:
        gc.scored = True
        gc.scorePlayer += 1

    #checking the player whom the ball's going to
    #left
    if gc.ball_x > data['wWidth'] / 2:
        if gc.ball_x + 15 > gc.opponent_x and\
            gc.ball_y + 15 > gc.opponent_y and\
            gc.ball_x - 15 < gc.opponent_x + 15 and\
            gc.ball_y - 15 < gc.opponent_y - 250:
            gc.ball_speed_x *= -1
    #right
    else:
        if gc.ball_x + 15 > gc.player_x and\
            gc.ball_y + 15 > gc.player_y and\
            gc.ball_x - 15 < gc.player_x + 15 and\
            gc.ball_y - 15 < gc.player_y - 250:
            gc.ball_speed_x *= -1

    #----------playerAnimation---------------
    if movement == 'upO':
        moveO = 10
    elif movement == 'downO' :
        moveO = -10
    elif movement == 'stopO':
        moveO = 0
    
    if movement == 'upP':
        moveP = 10
    elif movement == 'downP' :
        moveP = -10
    elif movement == 'stopP':
        moveP = 0
    
    gc.player_y += moveP
    gc.opponent_y += moveO
    #needs movement limitations up down checkReminder
    gc.save()
    return gc
#still needs up down protections
# await sync_to_async(initialize_msg_instance)(text_data_json)
# Send message to room group => show in room