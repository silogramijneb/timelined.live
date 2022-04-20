from django.shortcuts import render
from django.http import HttpResponse

from main.forms import EventCreationForm
from .forms import EventForm

# Sends user data from timeline event to database
def updateEvent(request, context):
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    context.update({"create_event_form": form})

def createEvent(request, context):
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    context.update({"create_event_form": form})

# Create your views here.
def dashboard(response):
    return render(response, "dashboard/home.html")

def timeline(request):
    
    context = {}
    context.update({"create_event_form": EventForm()})
    
    # POST: Update context
    if request.method == "POST":
        if request.POST.get("action") == 'update':
            updateEvent(request, context)

    # POST: Save Form
    if request.method == "POST":
        if request.POST.get("action") == 'submit':
            createEvent(request, context)
            
    result = render(request, "dashboard/timeline.html", context)            
    return result

def events():
    return render("dashboard/events.html")
