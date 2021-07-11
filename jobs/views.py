from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from .models import Job

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        jobs=Job.objects.filter(account__user__id=request.user.id)
        print(jobs)
        return (HttpResponse(jobs))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        

