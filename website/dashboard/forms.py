from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_bootstrap5.bootstrap5 import *

from .models import TimelineEvent
from main.models import Event

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
class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_date', 'end_date'] #'file']
        widgets = {
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Crispy Package Setup
        self.helper = FormHelper()

        # Set HTTP Request
        self.form_method = 'POST'

        # Bootstrap 
        self.helper.layout = Layout(
            FloatingField('name', css_class='mb-3'),
            FloatingField('text', 'description', css_class='mb-3'),
            FloatingField('location', css_class='mb-3'),
            FloatingField('start_date', css_class='mb_3'),
            FloatingField('end_date', css_class='mb_3'),
        )
