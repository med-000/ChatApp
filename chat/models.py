from django.db import models
from datetime import datetime
from datetime import date
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    nickname = models.CharField(max_length=1000,null = True,blank = True)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class MyProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user_id  = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    profile = models.CharField(max_length=100,null = True,blank = True)
    birthday = models.DateField(max_length=100,default=date(1950, 1, 1))
    room_ids = models.JSONField(default=list,null = True,blank = True)   
    avater = models.ImageField(upload_to='avatars/', null=True, blank=True)