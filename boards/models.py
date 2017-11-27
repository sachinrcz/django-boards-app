from django.db import models
from django.contrib.auth.models import  User

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    board = models.ForeignKey(Board, related_name='topics')
    subject = models.CharField(max_length=30)
    last_update = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, related_name='topics')

    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=1000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.message