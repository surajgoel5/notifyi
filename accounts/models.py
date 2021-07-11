from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
KEY_LENGTH=15
def generate_key(keylen=KEY_LENGTH):
        return ''.join(random.choice(string.hexdigits) for i in range(keylen))
class Account(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    key= models.CharField(max_length=KEY_LENGTH,default=generate_key )

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()