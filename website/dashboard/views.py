from django.shortcuts import render
from django.http import HttpResponse

from main.forms import EventCreationForm

# Sends user data from timeline event to database
def updateEvent(request, context):
    initial_data = {"name": "EVENT TITLE"}
    form = EventCreationForm(request.POST, initial_data=initial_data)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    context.update({"event_creation_form": form})

# Create your views here.
def dashboard(response):
    return render(response, "dashboard/home.html")

def timeline(request):
    
    context = {}
    context.update({"event_creation_form": EventCreationForm()})
    
    # POST: Update context
    if request.method == "POST":
        if request.POST.get("action") == 'update':
            updateEvent(request, context)
            
    result = render(request, "dashboard/timeline.html", context)            
    return result