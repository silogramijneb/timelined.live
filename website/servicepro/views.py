from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(response):
    return render(response, 'servicepro/dashboard_main.html')