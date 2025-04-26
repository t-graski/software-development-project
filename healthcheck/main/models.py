from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

class HealthCard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=[('green', 'Green'), ('amber', 'Amber'), ('red', 'Red')])
    progress = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)