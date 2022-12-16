from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.body[:50]


class Personalchat(models.Model):
    sender=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='sender')
    receiver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='receiver')
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.body[:50]


class VideocallMembers(models.Model):
    uid=models.IntegerField(null=True)
    name=models.CharField(max_length=200,null=True)
    channel=models.CharField(max_length=200)

    def __str__(self):
        return self.name