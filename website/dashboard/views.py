from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from main.forms import EventCreationForm
from main.models import *

# Sends user data from timeline event to database
def updateEvent(request, context):
    form = EventCreationForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    context.update({"form": form})

def createEvent(request, context):
    form = EventCreationForm(request.POST) 
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    context.update({"form": form})

# Create your views here.
def dashboard(response):
    context = {'timeline_list' : [1, 2, 3, 4, 5, 6, 7, 8],
                'teststring' : "CONTEXT WAS PASSED"}
    return render(response, "dashboard/home.html", context)


def timeline(request):

    context = {
        "form": EventCreationForm(request.POST),
        "maxEventNumbers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    }
    
    # POST: Update context
    if request.method == "POST":
        if request.POST.get("action") == 'update':
            updateEvent(request, context)

    # POST: Save Form
    if request.method == "POST":
        if request.POST.get("action") == 'createEvent':
            createEvent(request, context)
            
    result = render(request, "dashboard/timeline.html", context)            
    return result


'''
def timeline(request):
    context = {}
    if request.method == "POST":
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            event_title = form.cleaned_data.get('title')
            messages.success(request, f'{event_title} created!')
            
        context["form"] = form
        return render(request, "dashboard/timeline.html", context)
'''

def events():
    return render("dashboard/events.html")
