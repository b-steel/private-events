from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Event, Location

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'location')
        widgets = {
            'date': forms.DateInput(format='%m/%d/%y', attrs={
                'placeholder': 'MM/DD/YYYY'
            }), 
        }
        help_texts = {
            'date': 'Format: MM/DD/YYYY'
        }
