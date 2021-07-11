from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return (HttpResponse('accounts index? why you mere m8'))

