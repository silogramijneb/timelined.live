from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Timeline, Event


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'username', 'password1', 'password2', 'phone']

class TimelineCreationForm(ModelForm):
    class Meta:
        model = Timeline
        fields = ['name']

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'deadline', 'file']
        widgets = { 'timeline_id' : forms.HiddenInput 
                    }

        