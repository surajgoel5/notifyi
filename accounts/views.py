from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return (HttpResponse('User page with notifs will be here if logged in, lese login page'))

def sign_up(request):
    return HttpResponse('sign up')

def login(request):
    #return HttpResponse('login')
    return render(request,'login.html')
def logout(request):
    return HttpResponse('logged out' )

def change_password(request):
    return HttpResponse('change passy')