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
    if MyProfile.objects.filter(name = username):
            return redirect('mypage',username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        user_id = request.POST['user_id']
        nickname = request.POST['nickname']
        profile = request.POST['profile']
        birthday = request.POST['birthday']
        user = User.objects.get(username = username)
        email = user.email

        new_profile = MyProfile.objects.create(name = username, user_id = user_id, nickname = nickname, profile= profile, birthday = birthday,email = email)
        new_profile.save()

        return redirect('mypage',username)
    else:
        form = ProfileForm()
        return render(request,'profile/myprofile_add.html',{'form':form, 'username':username})

def myprofile_edit(request,username):
    profile = MyProfile.objects.get(name = username)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('mypage',username)
    else:
        form = ProfileForm(instance = profile)
    return render(request,'profile/myprofile_edit.html',{'username':username,'form':form})

def myprofile(request):
    return render(request,'profile/myprofile.html')
    
def mypage(request, username):
    user = User.objects.all()
    try:
        profile = MyProfile.objects.get(name=username)
    except MyProfile.DoesNotExist:
        profile = None

    return render(request, 'mypage.html', {
        'username': username,
        'user': user,
        'profile': profile,
    })

def personal_chat_add(request, username):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile = MyProfile.objects.get(name=username)
        nickname = profile.nickname

        if MyProfile.objects.filter(email=email).exists():
            youruser = MyProfile.objects.get(email = email)
            yournickname = youruser.nickname
            return redirect('profile', username=username, nickname=yournickname)

        else:
            messages.info(request, 'メールアドレスが存在しません')
            return render(request, 'chat/personal_chat_add.html', {'username': username})

    return render(request, 'chat/personal_chat_add.html', {'username': username})

def personal_chat_add_home(request,username,nickname):
    if request.method == "POST":
        yourprofile = MyProfile.objects.get(nickname = nickname)
        myprofile = MyProfile.objects.get(name = username)
        room = str(yourprofile.id) + '-' + str(myprofile.id)


        if Room.objects.filter(name=room).exists():
            return redirect('/home' + '/' + username +'/' + room +'/' + room)
        else:
            new_room = Room.objects.create(name=room,nickname = room)
            new_room.save()
            my_id_li = myprofile.room_ids or []
            your_id_li = yourprofile.room_ids or []
            id = new_room.id
            my_id_li.append(id)
            your_id_li.append(id) 
            yourprofile.room_ids = your_id_li
            myprofile.room_ids = my_id_li
            yourprofile.save()
            myprofile.save()
            return redirect('/home' + '/' + username +'/' + room +'/' + room)
    
    
    else:
        return render(request,'profile/profile.html',{'username':username, 'nickname':nickname})

def profile(request,username,nickname):
    profile = MyProfile.objects.get(nickname= nickname)
    nickname = profile.nickname
    email = profile.email
    user_id = profile.user_id
    yourprofile = profile.profile
    birthday = profile.birthday
    id = profile.id

    return render(request,'profile/profile.html',{'nickname':nickname,'username':username,'email':email ,'user_id':user_id,'yourprofile':yourprofile,'birthday':birthday,'id':id})

def group_chat_add(request,username):
    myprofile = MyProfile.objects.get(name = username)
    room_ids = myprofile.room_ids
    everyonefiles = []
    for profile in MyProfile.objects.all():
        if profile != myprofile: 
            if profile.room_ids:
                if any(room_id in profile.room_ids for room_id in room_ids):
                    everyonefiles.append(profile)
                    
    if request.method == 'POST':
        selected = request.POST.getlist('choices')
        request.session['selected'] = selected 
        return redirect('confirm', username=username)
    
    return render(request,'chat/group_chat_add.html',{'username':username,'everyonefiles':everyonefiles})

def confirm(request, username):
    if request.method == 'POST':
        selected = request.session.get('selected', [])
        return redirect('groupprofile', username=username)
    
    selected = request.session.get('selected', [])
    nicknames = []
    for select in selected:
        profile = MyProfile.objects.get(email = select)
        nickname = profile.nickname
        nicknames.append(nickname)
    return render(request, 'confirm.html', {
        'username': username,
        'nicknames': nicknames
    })

def groupprofile(request,username):
    if request.method == 'POST':
        nickname = request.POST['groupname']
        selected = request.session.get('selected',[])
        myprofile = MyProfile.objects.get(name = username)
        id = myprofile.id
        room = str(id)
        for select in selected:
            otherprofile = MyProfile.objects.get(email = select)
            everyoneid = str(otherprofile.id)
            room += "-" + everyoneid
        
        if Room.objects.filter(name=room).exists():
            return redirect('/home' + '/' + username +'/' + room +'/' + nickname)

        else:
            new_room = Room.objects.create(name = room,nickname = nickname)
            new_room.save()
            id = new_room.id
            myroom_ids = myprofile.room_ids
            myroom_ids.append(id)
            myprofile.room_ids = myroom_ids
            myprofile.save()
            for select in selected:
                otherprofile = MyProfile.objects.get(email = select)
                otherroom_ids = otherprofile.room_ids
                otherroom_ids.append(id)
                otherprofile.room_ids = otherroom_ids
                otherprofile.save()
            return redirect('/home' + '/' + username +'/' + room +'/' + nickname)


    return render(request,'profile/groupprofile.html',{'username':username}) 

def home(request,username):
    myprofile = MyProfile.objects.get(name = username)
    room_ids = myprofile.room_ids
    rooms = []
    roomsname = []
    yourprofile = None
    for room_id in room_ids or []:
        room = Room.objects.filter(id = room_id).first()
        if room:
            rooms.append(room)
            roomsname.append(room.name)
            room_li = room.name.split("-")
            if room.name == room.nickname:
                if int(room_li[0]) == myprofile.id:
                    confirm_your_id = room_li[1]
                    yourprofile = MyProfile.objects.get(id = confirm_your_id)
                elif int(room_li[1]) == myprofile.id:
                    confirm_your_id = room_li[0]
                    yourprofile = MyProfile.objects.get(id = confirm_your_id)
                else:
                    pass

    return render(request, 'home.html',{'username':username,'roomsname':roomsname,'rooms':rooms,'myprofile':myprofile,'yourprofile':yourprofile})

def room(request, room, username, nickname):
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'nickname':nickname,
    })

def checkview(request,username):
    room = request.POST['room_name']

    if Room.objects.filter(name=room).exists():
        return redirect('/home' + '/' + username +'/' + room)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/home' + '/' + username +'/' + room)

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