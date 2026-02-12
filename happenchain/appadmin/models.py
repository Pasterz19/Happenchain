from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)
    against = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue} - {self.user.username}"
