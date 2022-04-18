from django.shortcuts import render
from django.http import HttpResponse
from main.models import *

# These functions route the HTML in the templates folder to the correct view

# Common queries can be done using Classname.objects.filter(condition)

# Get the client object based on the username
def getClient(username):
    Client.objects.filter(user_name = username)

# Get the service provider object based on the username
def getSP(username):
    ServiceProvider.objects.filter(user_name = username)

# Get the third party object based on the username
def getTP(username):
    ThirdParty.objects.filter(user_name = username)

### Define more functions for queries (Not sure if this is the right file for this)

def index(response):
    return render(response, 'main/index.html')
