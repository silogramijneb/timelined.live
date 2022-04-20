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
            'title', 'event_type', 'description', 'status', 'location',
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                FloatingField("event_title", css_class="mb-3"),
                FloatingField("event_type", css_class="mb-3"),
                FloatingField("event_description", css_class="mb-3"),
                FloatingField("status", css_class="mb-3"),
                FloatingField("dependent_on", css_class="mb-3"),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class="button white")
                ),
        )
