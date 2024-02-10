from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Chat(models.Model):
    name = models.CharField(max_length=100)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.name
