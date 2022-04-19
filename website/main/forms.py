from dataclasses import field
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ThirdParty, ServiceProvider, Client, Timeline, Event
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit  
from crispy_bootstrap5.bootstrap5 import FloatingField

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email Address',
        } # Password1 and Password2 must be relabled outside of lables

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Crispy Package Setup
        self.helper = FormHelper()

        # Bootstrap 
        self.helper.layout = Layout(
            FloatingField('first_name', css_class='mb-3'),
            FloatingField('last_name', css_class='mb-3'),
            FloatingField('date_of_birth', css_class='mb-3'),
            FloatingField('email', css_class='mb-3'),
            FloatingField('password1', css_class='mb-3'),
            FloatingField('password2', css_class='mb-3'),
            Div(
                Submit('submit', 'register', css_class='btn btn-primary rounded-pill btn-lg', label='Register'),
                css_class='d-grid'
            )
        )

        # Submission 
        # self.helper.add_input(Submit('submit', 'Submit'))

            
        # Django form attributes / Field properties
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = 'Password Confirmation'
        self.fields['date_of_birth'].widget = DateInput()



class ProfessionalRegistrationForm(UserCreationForm):
    class Meta:
        model = ServiceProvider
        fields = ['first_name', 'last_name', 'provider_name', 'website', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email Address',
        } # Password1 and Password2 must be relabled outside of lables

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Crispy Package Setup
        self.helper = FormHelper()

        # Bootstrap 
        self.helper.layout = Layout(
            FloatingField('first_name', css_class='mb-3'),
            FloatingField('last_name', css_class='mb-3'),
            FloatingField('provider_name', css_class='mb-3'),
            FloatingField('website', css_class='mb-3'),
            FloatingField('email', css_class='mb-3'),
            FloatingField('password1', css_class='mb-3'),
            FloatingField('password2', css_class='mb-3')
        )
            
        # Django form attributes / Field properties
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = 'Password Confirmation'

class ThirdPartyRegistrationForm(UserCreationForm):
    class Meta:
        model = ThirdParty
        fields = ['first_name', 'last_name', 'third_party_name', 'website', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email Address',
        } # Password1 and Password2 must be relabled outside of lables

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Crispy Package Setup
        self.helper = FormHelper()

        # Bootstrap 
        self.helper.layout = Layout(
            FloatingField('first_name', css_class='mb-3'),
            FloatingField('last_name', css_class='mb-3'),
            FloatingField('third_party_name', css_class='mb-3'),
            FloatingField('website', css_class='mb-3'),
            FloatingField('email', css_class='mb-3'),
            FloatingField('password1', css_class='mb-3'),
            FloatingField('password2', css_class='mb-3')
        )
            
        # Django form attributes / Field properties
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = 'Password Confirmation'
        self.fields['third_party_name'].label = 'Third Party Name'


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