from django.db import models
from accounts.models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver


class Job(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ping_time=models.DateTimeField(auto_now_add=True)
    origin_device=models.CharField(max_length=50,blank=True)
    message=models.CharField(max_length=200,default='Job is Complete')
    title=models.CharField(max_length=50,default='Untitled Job')

    def __str__(self):
        return f'Job#{self.id} for {self.account.user.username}: {self.title}' 