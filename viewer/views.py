from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, ChatRoom
from faker import Faker


fake = Faker()

def main(request):
    statistic_groups = Statistic.objects.all()
    chat_rooms = ChatRoom.objects.all()
    if request.method == 'POST':
        if request.POST.get('new-statistic'):
            new_statistic = request.POST.get('new-statistic')
            obj, _ = Statistic.objects.get_or_create(name=new_statistic)
            return redirect('dashboard', obj.slug)
        if request.POST.get('new-chat-room'):
            new_chat_room = request.POST.get('new-chat-room')
            obj, _ = ChatRoom.objects.get_or_create(name=new_chat_room)
            return redirect('chat_room', obj.name)
    context = {
        'statistic_groups': statistic_groups,
        'chat_rooms': chat_rooms
    }
    return render(request, 'main.html', context)


def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    context = {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    }
    return render(request, 'dashboard.html', context)


def chat_room(request, name):
    obj = get_object_or_404(ChatRoom, name=name)
    context = {
        'name': obj.name,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    }
    return render(request, 'chatroom.html', context)



