from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'date_of_birth', 'username', 'password1', 'password2', 'phone']

class ProfessionalRegistrationForm(UserCreationForm):
    class Meta:
        model = ServiceProvider
        fields = ['first_name', 'last_name', 'provider_name', 'website', 'username', 'password1', 'password2']

class ThirdPartyRegistrationForm(UserCreationForm):
    class Meta:
        model = ThirdParty
        fields = ['first_name', 'last_name', 'third_party_name', 'website', 'username', 'password1', 'password2']

class TimelineCreationForm(ModelForm):
    class Meta:
        model = Timeline
        fields = ['name']

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'deadline', 'file']
        widgets = { 'timeline_id' : forms.HiddenInput }

        