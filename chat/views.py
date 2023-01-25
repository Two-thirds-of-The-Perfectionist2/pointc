from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse

from chat.models import Room, Message


def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    print(room)
    print(Room.objects.filter(name=room))
    room_details = get_object_or_404(Room , name=room)
    return render(request, 'room.html', {
        'username':username,
        'room':room,
        'room_details':room_details}
        )


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if not Room.objects.filter(name=room).exists():
        new_room = Room.objects.create(name=room)
        new_room.save()
    return redirect(room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = get_object_or_404(Room , name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
