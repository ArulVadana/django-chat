from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RoomForm,SignUpform,ProfileForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message,Personalchat,VideocallMembers
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import time
import json
import os

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST['username'].lower()
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User doesn't exist")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
    
    context={'page':page}
        
    return render(request,'chat/login-page.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=SignUpform()
    context={'form':form}

    if request.method == 'POST':
        form=SignUpform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'error occured {form.errors}')

    return render(request,'chat/login-page.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ""
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|
                            Q(name__icontains=q)|
                            Q(description__icontains=q))
    topics=Topic.objects.all()
    room_count=rooms.count()
    users=User.objects.all()
    context={'rooms':rooms,"topics":topics,'room_count':room_count,"users":users}
    return render(request, 'chat/home.html',context)

def room(request,pk,room_name):
    room=Room.objects.get(id=int(pk))
    room_messages=room.message_set.all()
    participants = room.participants.all()
    
    if request.method=='POST':
        room_message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id,room_name=room.name)
    context={"room":room,"room_messages":room_messages,"participants":participants}
    return render(request, 'chat/room.html',context)

@login_required(login_url='login-page')
def Userprofile(request,pk):
    profile=User.objects.get(id=int(pk))
    rooms = Room.objects.filter(host=profile)
    users=User.objects.all()

    context={"profile":profile,"users":users,"rooms":rooms}
    return render(request,'chat/profile.html',context)

@login_required(login_url='login-page')
def UserprofileUpdate(request,pk):
    user=User.objects.get(id=int(pk))
    form=ProfileForm(instance=user)

    if request.method == 'POST':
        form=ProfileForm(request.POST,instance=user)
        user.username=request.POST.get('username')
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        user.save()
        return redirect('home')
        

    context={"user":user,"form":form}

    return render(request,'chat/profile_update.html',context)

@login_required(login_url='login-page')
def PersonalChatRoom(request,pk1,pk2,room_name):
    chats=Personalchat.objects.filter(Q(sender=int(pk1),receiver=int(pk2))|Q(sender=int(pk2),receiver=int(pk1)))
    if request.user.id == int(pk1):
        person= User.objects.get(id=int(pk2))
    else:
        person=User.objects.get(id=int(pk1))

    if request.method=='POST':
        chat=Personalchat.objects.create(
            sender=request.user,
            receiver=person,
            body=request.POST.get('body')
        )
        return redirect('personal-chat',pk1=request.user.id,pk2=person.id,room_name=person.username)
        

    context={"chats":chats,"person":person,}
    return render(request,'chat/person-chat.html',context)


@login_required(login_url='login-page')
def createRoom(request):
    form=RoomForm()
    topic=Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context={'form':form,'topic':topic}
    return render(request,'chat/room-form.html',context)

@login_required(login_url='login-page')
def updateRoom(request,pk):
    room=Room.objects.get(id=int(pk))
    form=RoomForm(instance=room)
    topic=Topic.objects.all()
    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
            
        return redirect('home')

    context={'form':form,'topic':topic,'room':room}
    return render(request,'chat/room-form.html',context)

@login_required(login_url='login-page')
def deleteRoom(request,pk):
    room=Room.objects.get(id=int(pk))

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'chat/delete-room.html',context)



@login_required(login_url='login-page')
def videoCall(request,pk):
    room=Room.objects.get(id=int(pk))
    return render(request,'chat/video_call.html',{'room':room})

@login_required(login_url='login-page')
@csrf_exempt
def getToken(request):
    appId = os.environ.get("APP_ID")
    appCertificate = os.environ.get("APP_CERTIFICATE")
    print(appId)
    channelName = request.GET.get('channel')
    uid=request.user.id
    role = 1
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    VideocallMembers.objects.create(
        uid=request.user.id,
        name=request.user,
        channel=request.GET.get('channel'),
    )

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@login_required(login_url='login-page')
def usernameVideocall(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member=VideocallMembers.objects.get(uid=uid,channel=room_name)

    return JsonResponse({'name':member.name}, safe=False)

@login_required(login_url='login-page')
@csrf_exempt
def userdelVideo(request):
    data = json.loads(request.body)
    try:
        member = VideocallMembers.objects.get(uid=int(data['UID']),channel=data['room_name'])
        member.delete()

    except Exception:
        print(Exception)
    return JsonResponse('Member deleted', safe=False)
