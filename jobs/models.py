from django.db import models
from accounts.models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver
from webpush import send_group_notification
from django.contrib.staticfiles import finders
from django.templatetags.static import static



class Job(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ping_time=models.DateTimeField(auto_now_add=True)
    origin_device=models.CharField(max_length=50,blank=True)
    message=models.CharField(max_length=200,default='Job is Complete')
    title=models.CharField(max_length=50,default='Untitled Job')

    def __str__(self):
        return f'Job#{self.id} for {self.account.user.username}: {self.title}' 

    def send_notif(self):
        icon = static('/favicon.png')
        badge = 'https://notifyi.herokuapp.com/static/badge.png'#static('/badge.png')
       # print(badge)
        payload = {"head": self.title, "body": self.message,"icon":icon, "badge": badge}
        send_group_notification(group_name=self.account.user.username, payload=payload, ttl=1000)


