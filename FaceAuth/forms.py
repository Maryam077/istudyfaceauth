"""
lib imports
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from .utils import base64_file
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit

"""
Registration form
"""
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    image = forms.CharField(max_length=500,widget = forms.HiddenInput(), required=True)
    helper = FormHelper()
    helper.add_input(Button('verify', 'Verify Face', css_class='btn-primary', required=True, onclick="verifyface()"))
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-outline-info'))
    helper.form_method = 'POST'
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserRegisterForm, self).save(commit=True)
        face_image = UserProfile(user=user, photo=self.data['image'])
        face_image.save()
        return user

"""
Authentication
"""
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length = 100,required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    #image = forms.CharField(max_length=500,widget = forms.HiddenInput(), required=True)
    helper = FormHelper()
    #helper.add_input(Button('verify', 'Verify Face', css_class='btn-primary', required=True, onclick="face_auth()"))
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-outline-info',onsubmit=" return false;face_auth();"))
    helper.form_method = 'POST'
       