from django.shortcuts import render, redirect
from chat.models import Room, Message,MyProfile
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import os
from .forms import ProfileForm


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password )

        if user is not None:
            auth.login(request,user)
            return redirect('myprofile_add',username=username)
        else:
            messages.info(request,'ログイン情報が間違っています')
            return redirect('login')
    
    else:
        return render(request, "login.html")
    

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "メールが既に使われています")
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, "ユーザー名が既に使われています")
                return redirect('register')
            else:
                user = User.objects.create_user(username = username , email = email , password = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'パスワードが一致しません')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def myprofile_add(request,username):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        nickname = request.POST['nickname']
        profile = request.POST['profile']
        birthday = request.POST['birthday']
        
        new_profile = MyProfile.objects.create(name = username, user_id = user_id, nickname = nickname, profile= profile, birthday = birthday)
        new_profile.save()

        return redirect('mypage',username)
    else:
        form = ProfileForm()
    return render(request,'profile/myprofile_add.html',{'form':form, 'username':username})

def myprofile_edit(request):
    return render(request,'profile/myprofile_edit.html')

def myprofile(request):
    return render(request,'profile/myprofile.html')
    
def mypage(request,username):
    user = User.objects.all()
    return render(request,'mypage.html',{'username':username,'user':user})

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})