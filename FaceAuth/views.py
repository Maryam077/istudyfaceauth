from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.conf import settings
from .utils import prepare_image, face_detect, match_face
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
import threading
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import datetime

def index(request):
    if request.user.is_authenticated  :
        checkloggedin(request.user)
    return render(request,'index.html',{})

def checkloggedin(user):
    lastloginminutes = int(((timezone.now() - user.last_login).total_seconds())/60)%60
    if lastloginminutes > 1:
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') and  data.get('_auth_user_id') == str(user.id):
                print('matching')
                print(user)
                match_face(user,True)
                threading.Timer(15.0,checkloggedin,args=(user,)).start()
        
def register(request):
    #face_detect('')

    if  request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User '+username+' created successfully!')
        
            return render(request, 'registration/login.html', context={'form': UserLoginForm()})
            #return redirect(settings.LOGIN_REDIRECT_URL)
        elif len(form.data['image']) == 0:
            messages.add_message(request, messages.ERROR, 'Face verification required!')
        else:
            print('psst',form.data['image'])

    else:
        form = UserRegisterForm()


    return render(request, 'registration/register.html', context={'form': form})

def login_page(request):
    if request.user.is_authenticated:
           return redirect('index')

    if  request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            #print('user',user.userprofile.photo)
            if user:
                # print(user.userprofile_set.all())
                if face_auth_view(user):
                    login(request, user)
                    return redirect('index')
                else:
                    messages.add_message(request, messages.ERROR, 'Face verification failed please try again!')
            else:
                   messages.add_message(request, messages.ERROR, 'Crededentials mismatch!')
        #elif len(form.data['image']) == 0:
        #    messages.add_message(request, messages.ERROR, 'Face verification required!') 
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', context={'form': form})

def face_detect_view(request):
    x = face_detect()
    return JsonResponse({'data': x})

def face_auth_view(user):
    x = match_face(user,True)
    print (x)
    return x

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
    
