from django.shortcuts import render
from django.http import HttpResponse

# These functions route the HTML in the templates folder to the correct view

def index(response):
    return render(response, 'main/index.html')
