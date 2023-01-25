from decouple import config
from django.shortcuts import redirect

from chat.models import Room


def roomname():
    from django.utils.crypto import get_random_string


    code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOASDFGHJKLZXCVBNM234567890')

    return code


def chatroom(room, username):
    new_room = Room.objects.create(name=room)
    new_room.save()
    
    return f"http://{config('CURRENT_HOST')}/chat/{room}/?username={username}"
