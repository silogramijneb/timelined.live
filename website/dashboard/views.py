from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(response):
    return render(response, "dashboard/home.html")

def timeline(response):
    return render(response, "dashboard/timeline.html")