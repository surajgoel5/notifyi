from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from .models import Job
from accounts.models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        jobs=Job.objects.filter(account__user__id=request.user.id)
        webpush = {"group": request.user.username } # The group_name should be the name you would define.
        return render(request, 'job_home.html', {'jobs': jobs,'user':request.user,"webpush":webpush})
        
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def disp_user_key(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.account.key)
        
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


@csrf_exempt 
def job_request(request):
    if request.method=="POST":
        try:
            in_key=request.POST.get("key")
            in_username=request.POST.get("username")
        except:
            return HttpResponse(status=400) # Bad Request
        acc=Account.objects.filter(key=in_key, user__username=in_username)
        if len(acc)<1:
            return HttpResponse(status=401) # Unauthorized
        elif len(acc)>1:
            return HttpResponse(status=500) #Internal Server Error
        else:
            title=request.POST.get("title")
            message=request.POST.get("message")
            origin_device=request.POST.get("origin_device")
            if title is None:
                title='Untitled Job'
            if message is None:
                message='Job Completed.'
            if origin_device is None:
                origin_device='Unknown'    
            
            job=Job(account=acc[0],title=title, message=message,origin_device=origin_device)

            job.save()
            job.send_notif()
        
        return HttpResponse(status=200)# OK
    else :
        return HttpResponse(status=400) # Bad Request
   




@csrf_exempt 
def verify_key(request):
    valid=False
    user=''
    found=False
    error='None'
    if request.method=="POST":
        valid=True
        in_key=request.POST.get("key")
        acc=Account.objects.filter(key=in_key)
        if len(acc)<1:
            found=False
        elif len(acc)>1:
            error='Multiple Users Found'
        else:
            found=True
            user=acc[0].user.username
        
    return JsonResponse({'username':user,'valid_request':valid,'found':found,'error':error})
   

