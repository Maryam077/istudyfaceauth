from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.conf import settings
from .utils import prepare_image, face_detect, face_auth
from django.http import JsonResponse, HttpResponse



# Create your views here.
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
           return HttpResponse('Welcome '+ request.user.username)
    if  request.method == 'POST':
        if request.user.is_authenticated:
            HttpResponse('Welcome '+ request.user.username)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            #print('user',user.userprofile.photo)
            if user:
                if face_auth_view(user.userprofile.photo, user.username):
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'User '+username+' logged in successfully!')
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

def face_auth_view(location, username):
    print(location)
    x = face_auth(location, username)
    print (x)
    return x
