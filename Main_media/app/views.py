from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
# Create your views here.
def main(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                Q(topic__name__icontains=q) |
                Q(name__icontains=q)
    ).annotate(cnt=Count('participants'))

    topics = Topic.objects.annotate(cnt=Count('room')).filter(cnt__gt=0)
    all = Topic.objects.aggregate(cnt=Count('room'))
    # count_room = rooms.count()
    last_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[:5]

    context = {'rooms': rooms, 'topics': topics, 'all': all, 'activities': last_messages}
    return render(request, 'app/index.html', context)

def getRoom(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()


    if request.method == "POST":
        if request.user in participants:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
        else:
            room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'members': participants}
    return render(request, 'app/room.html', context)

def getUser(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    cnt = rooms.count()
    last_messages = Message.objects.filter(user__id = pk).order_by('-created')[:5]
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'activities':last_messages, 'cnt': cnt, 'topics': topics}
    return render(request, 'app/profile.html', context)


def getExit(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    if request.method == 'POST':
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'app/join.html', )


def getTopic(request, pk):
    rooms = Room.objects.filter(topic_id = pk)
    topic = Topic.objects.get(id = pk)
    context = {'rooms': rooms, 'topic': topic}
    return render(request, 'app/get_topic.html', context)

@login_required(login_url='/login')
def createRoom(request):

    if request.method == 'POST':
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     print(request.POST.get('topic'))
        #     form.save()
        #     return redirect('main')
        topic = Topic.objects.get(id=request.POST.get('topic'))
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            content=request.POST.get('content')
        )
        return redirect('main')
    else:
        form = RoomForm()
    context = {'form': form, 'action': 'create'}
    return render(request, 'app/roomForm.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('<h2>You arent allowed here!</h2>')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('main')
    context = {'form': form, 'action': 'update'}
    return render(request, 'app/roomForm.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('<h2>U arent allowed here!</h2>')

    if request.method == 'POST':
        room.delete()
        return redirect('main')
    return render(request, 'app/delete.html', {'obj': room})

def loginUser(request):
    page = 'login'
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You success login!')
            return redirect('main')
        else:
            messages.error(request, 'username or password doesnt exist!')
    else:
        form = LoginForm()
    context = {'form': form, 'action': 'Login'}
    return render(request, 'app/login-register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'you logged out!')
    return redirect('main')

def registerUser(request):
    page = 'register'
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created!')
            return redirect('main')
        else:
            messages.error(request, 'You have error(s)!')
    else:
        form = RegisterForm()
    context = {'form': form, 'action': 'register'}
    return render(request, 'app/login-register.html', context)


@login_required(login_url='login/')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('<h2>U arent allowed here!</h2>')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.pk)
    return render(request, 'app/delete.html', {'obj': message})

@login_required(login_url='login/')
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse('<h3>You dont have permission</h3>')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('room', pk=message.room.pk)

    context = {'form':form, 'action': 'change'}
    return render(request, 'app/roomForm.html', context)
