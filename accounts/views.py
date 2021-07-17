from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def index(request):
    return (HttpResponse('accounts index? why you mere m8'))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
    else:
        form = UserCreationForm()
        form.fields['username'].help_text+='Case Sensitive!'
    #print(form.error_message)   
    return render(request, 'registration/signup.html', {'form': form})

