from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_bootstrap5.bootstrap5 import *

from .models import TimelineEvent
from main.forms import EvenCreationForm

'''
class EventForm(ModelForm):
    
    class Meta:
        model = TimelineEvent
        fields = [ 'title', 'description' ]
        labels = {
            'title': 'Event Title',
            'description': 'Description',
        }
        exclude = ['date_created', 'date_last_modified', 'date_completed', 'timeline']
'''