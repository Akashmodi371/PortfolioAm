from dataclasses import field
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from .models import Blog

from blog.models import Blog

#################### USer Sign Up #################
class SignUpForm(UserCreationForm):
    password2=forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels = {'email':'Email'}


################# Normal User Profile #################
class EditProfile(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','date_joined','last_login']
        labels={'email':'Email'}

################# For Admin Profile ###################
class EditAdminProfile(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields='__all__'
        labels={'email':'Email'}


############# BLog Form ###########################

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=['title','description']

