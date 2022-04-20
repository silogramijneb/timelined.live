from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_bootstrap5.bootstrap5 import *
from .models import TimelineEvent

class EventForm(ModelForm):
    
    class Meta:
        model = TimelineEvent
        fields = [
            'title', 'description', 'location',
            'timeline', 'file_upload'
        ]
        labels = {
            'title': 'Event Title',
            'event_type': 'Type of Event', 
            'description': 'Description',
            'status': 'Event Status',
            'location': 'Address',
            'timeline': 'Timeline',
            'file_upload': 'Upload Documents',
        }
        exclude = ['date_created', 'date_last_modified', 'date_completed', 'timeline']
