from django.db import models
from django.contrib.auth.models import User

class Task_model(models.Model):
    assigned_to = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, default="Medium")
    status = models.CharField(max_length=20, default="Pending")
    due_date = models.DateField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.assigned_to if self.assigned_to else 'Unassigned'}"