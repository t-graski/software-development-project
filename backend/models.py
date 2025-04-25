from django.db import models
from django.contrib.auth.models import User

# Represents a single sprint or retrospective session (e.g., Sprint 1, Sprint 2)
class Session(models.Model):
    name = models.CharField(max_length=100)  # Name of the session (e.g., "Sprint 1")
    date = models.DateField()  # When the session took place

    def __str__(self):
        # Display format for dropdowns and admin
        return f"{self.name} - {self.date}"

# Represents a health check card (e.g., Code Quality, Teamwork, Delivering Value)
class HealthCard(models.Model):
    title = models.CharField(max_length=100)  # Title of the health card

    def __str__(self):
        return self.title  # Shown in dropdowns and admin

# Represents a user's vote on a specific health card during a session
class Vote(models.Model):
    # Dropdown choices for traffic light voting system
    VOTE_CHOICES = [('green', 'Green'), ('amber', 'Amber'), ('red', 'Red')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who cast the vote
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # Which session it belongs to
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)  # Which area it's about
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)  # Traffic light choice
    progress = models.BooleanField()  # True = squad feels it's improving; False = same or worse

    def __str__(self):
        # Used in Django admin to show vote summary
        return f"{self.user.username} - {self.session.name} - {self.health_card.title}"
