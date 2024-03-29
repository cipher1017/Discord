from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


# rooms = [
#    {'id': 1, 'name': 'discussions'},
#    {'id': 2, 'name': 'develop'},
#    {'id': 3, 'name': 'design'},
# ]
def LoginPage(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        #get username and password
        username= request.POST.get('username').lower
        password= request.POST.get ('password')
#check if user exists
        try:
            user= User.objects.get(username=username)

        except:
            messages.error(request, 'user  is not registered')
            

        user = authenticate (request, username=username, password= password) 
        if user is not None:
            login(request, user)
            return redirect('home') 
            #if user is not logged in 
        else:
            messages.error(request, 'username or password does not exist')     

    context={'page':page}
    return render(request, 'base/login_register.html', context)
def logoutUser(request):

    logout(request)
    return redirect('home')

def registerPage(request):
    form= UserCreationForm
    context={'form':form}

    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            #we login the user
            login(request, user)
            return redirect(home)

        else:
            messages.error(request, 'an error occured while registering ')    

    
    return render(request, 'base/login_register.html', context)    
def home(request, ):
    q= request.GET.get ('q') if request.GET.get('q') !=None else ''
    rooms = Room.objects.filter(
        #adding a search parameter where we can search using either name of the host,topic or description]
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))


    topic= Topic.objects.all()
    room_count=rooms.count()
    context = {'rooms': rooms, 'topics':topic, 'room_count':room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    #comments center getting the children of all messages in a certain room
    room_messages = room.message_set.all().order_by('-created')
    participants=room.participants.all()

    if request.method== 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages':room_messages,'participants':participants}

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    #prefilling
    form= RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are hh git not allowed to make changes here")

    if request.method=='POST' :
        form= RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form': form}
    return render(request,'base/room_form.html', context )

@login_required(login_url='login')
def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not allowed to delete if you are not the host")


    if request.method== 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})
    
