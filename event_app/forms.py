from django import forms
from django.contrib.auth.models import User

from .models import Event

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'phoneno','event_type', 'location', 'date', 'venue']



class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'phoneno', 'event_type', 'location', 'date', 'venue']