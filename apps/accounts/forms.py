from django import forms
from django.contrib.auth.models import User

from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_username(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError(
            _('%(value)s is not a valid username'),
            params={'value': username},
        )

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True, validators=[validate_username])

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)

    
