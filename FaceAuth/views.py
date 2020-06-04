from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm, UserAuthenticationForm
from django.conf import settings
from .utils import prepare_image, face_detect
from django.http import JsonResponse



# Create your views here.
def register(request):
    #face_detect('')

    if  request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['image'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            messages.add_message(request, messages.SUCCESS, 'User '+username+' created successfully!')
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return render(request, 'registration/register.html', context={'form': UserRegisterForm()})
            #return redirect(settings.LOGIN_REDIRECT_URL)
        elif len(form.data['image']) == 0:
            messages.add_message(request, messages.ERROR, 'Face verification required!')
        else:
            print('psst',form.data['image'])

    else:
        form = UserRegisterForm()


    return render(request, 'registration/register.html', context={'form': form})

def face_detect_view(request):
    x = face_detect('')
    return JsonResponse({'data': x})
