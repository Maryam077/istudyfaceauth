"""
lib imports
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from .utils import base64_file

"""
Registration form
"""
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserRegisterForm, self).save(commit=True)
        image = base64_file(self.data['image'])
        face_image = UserProfile(user=user, image=image)
        face_image.save()
        return user

"""
Authentication
"""
class UserAuthenticationForm(AuthenticationForm):
    image = forms.CharField(widget=forms.HiddenInput())