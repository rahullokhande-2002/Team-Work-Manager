from django.db import models
from django.contrib.auth.models import User

class Task_model(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return self.title