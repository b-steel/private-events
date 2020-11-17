from django import forms
from .models import User
from django.forms import ModelForm

class SigninForm(forms.Form):
    pass

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)

    
