from asyncio import events
from atexit import register
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main.models import User, Client, ServiceProvider, ThirdParty, Timeline, Event
from .forms import ThirdPartyRegistrationForm, ClientRegistrationForm, ProfessionalRegistrationForm, TimelineCreationForm, EventCreationForm
from .decorators import unauthenticated_user 
from .enums import EventStatus
import json, random


# These functions route the HTML in the templates folder to the correct view

# Common queries can be done using Classname.objects.filter(condition)

# Get unique ID based on model
def generateID(model):
    newID = -1
    while (model.objects.filter(id=newID).first() is not None):
        newID = random.getrandbits(32)
    return newID

# Get the client object based on the id
def getTimeline(timeline_id):
    return Timeline.objects.get(id=timeline_id)

# Get the client object based on the username
def getClient(username):
    Client.objects.filter(user_name = username)

# Get the service provider object based on the username
def getSP(username):
    ServiceProvider.objects.filter(user_name = username)

# Get the third party object based on the username
def getTP(username):
    ThirdParty.objects.filter(user_name = username)

#### Authentication functions

# Validate registration data and add user to DB if valid 
def registerUser(response): 
    form = ClientRegistrationForm(response.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.id = generateID(User)
        user.email = user.username
        user.save()
        # Set user's permissions
            # Group logic
        login(response, user)
        return redirect('dashboard')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid registration data'})) 
        
# Valididate attempted user signin. Will redirect if valid
def signinUser(response):
        username = response.POST.get('username')
        password = response.POST.get('password')

        user = authenticate(response, username=username, password=password)
        message = 'Invalid email or password.'
            
        if user is not None:
            # Logic should be implemented to direct user based on their role
            login(response, user)
            return redirect('dashboard')
        else:
            return HttpResponse(json.dumps({'message': message}))

# Logout current user and send them back to homepage
def signoutUser(request):
    logout(request)
    return redirect('index')

### Timeline management functions

# Used to finilize a timeline. Assumes timeline is contained in our post
def createTimeline(request, context): 
    form = TimelineCreationForm(request.POST)
    message = 'Invalid timeline name.'
    ret = HttpResponse(json.dumps({'message': message}))

    # Validating and storing form data as model
    # POST contains name
    if(Event.objects.filter(timeline=timeline).count() > 0): # Check if timeline has events
        if form.is_valid():
            ret = redirect('dashboard') # On a sucessful timeline creation, we return to dash instead of return JSON
            timeline = form.save(commit=False) 
            timeline.save()
    else:
        message = 'Timeline must have at least 1 event.'
        ret = HttpResponse(json.dumps({'message': message}))
    
    return ret
    # context.update({"timeline_form":  form})

# NOTE: Heavily commented. Good example to look at for creating froms
# Form for creating an event. Assumes timeline is contained in our post
def createEvent(request, context): 
    form = EventCreationForm(request.POST)
    message = 'Invalid event details.'

    # Validating and storing form data as model
    if form.is_valid(): # PROVIDED: Name, Description, Location, Deadline.
                        #           Date Created and Date Modified are out generated.
                        #           POST will contain timeline.
        
        # Validation message
        message = 'Event has been added.'
        # Map form data to Timeline object
        event = form.save(commit=False) 

        # Enter requrired non-provided data
        # NOTE: While ID is a unique value for an event. 
        #       Index is it's index relative to the timeline
        event.id = generateID(Event)
        event.timeline = getTimeline(form.cleaned_data.get('timeline'))
        event.index = getTimeline(Timeline)
        event.status = EventStatus.NOT_STARTED

        # Add timeline to Database
        event.save()

    # Return an error or validation message depending on succes
    return HttpResponse(json.dumps({'message': message}))
    # context.update({"event_form":  form})


### Define more functions for queries (Not sure if this is the right file for this)

def index(response):
    # Defult context for our page
    context = { "registration_form":  ProfessionalRegistrationForm() }
    # Render defult page with updated context
    result = render(response, 'templates/index.html', context) 

    # POST: Update Context
    if response.method == 'POST':
        # On Service Pro registration, update form fields
        if response.POST.get('accountType') == 'servicePro':
            context.update({"registration_form":  ProfessionalRegistrationForm()})
            return # Assuming AJAX or some means of updating our form without refresh exists
        # On Third Party registration, update form fields
        if response.POST.get('accountType') == 'thirdParty':
            context.update({"registration_form":  ThirdPartyRegistrationForm()})
            return # Assuming AJAX or some means of updating our form without refresh exists
        # On Client registration, update form fields
        if response.POST.get('accountType') == 'client':
            context.update({"registration_form":  Client()})
            return # Assuming AJAX or some means of updating our form without refresh exists

    # POST: Update Render
    # Functions in this category will either return a JSON containing an error message
    if response.method == 'POST':
        # On registration submission attempt to create user
        if response.POST.get('action') == 'register':
            registerUser(response)
        # On signin submission attempt to signin user
        if response.POST.get('action') == 'login':
            result = signinUser(response)

    # Refresh Page, Redirect Page, or provide a JSON containing an error message
    return result

# A method that should be called strictly when the user begins the process of creating a timeline
# If user finishes making a timeline, timeline() should be called instead.
# When pressed, an empty timeline is created and the timeline id is passed back to the front end
# NOTE: Place holder name and URL
def maketimeline(response):
    timeline = Timeline.objects.create(id=generateID(Timeline))
    timeline.save()
    
    context = {"timeline" : locals().get('timeline')}
   
    # Return the timeline to the front end
    return render(response, 'templates/index.html', context)

# TODO: redirect dashboard to specific app template dashboard
def dashboard(response):
    return render(response, 'servicepro/dashboard_main.html')

