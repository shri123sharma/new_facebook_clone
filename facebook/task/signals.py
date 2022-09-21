from pdb import Pdb
import pdb
from turtle import pd
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FriendList, ProfileUpload
 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:

        ProfileUpload.objects.create(profileuser=instance)

@receiver(post_save,sender=FriendList)
def post_save_add_to_friends(sender,instance,created,**kwrags):
    sender_=instance.user
    receiver_=instance.friend
    if instance.status=='accepted':
        # import pdb;pdb.set_trace()
        ProfileUpload.objects.filter(profileuser=sender_).first().friends.add(receiver_)
        ProfileUpload.objects.filter(profileuser=receiver_).first().friends.add(sender_)

    else:
        instance.status='send'
        


        
