# models.py in iot_app
from django.contrib.auth.models import User
from django.db import models


class ReceivedMessage(models.Model):
    topic = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.topic}: {self.message}"
