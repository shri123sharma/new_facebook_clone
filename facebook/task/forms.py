from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.forms import ModelForm
from.models import *

class NewUserForm(UserCreationForm):
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    email=forms.EmailField(required=True)  
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

class PostUpload(forms.ModelForm):
    class Meta:
        model=Post
        fields='__all__'

class profileupload(forms.ModelForm):
    class Meta:
        model=ProfileUpload
        fields=['bio','detail','hobbies']
   

