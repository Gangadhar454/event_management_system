from django.db import models
from .event import Event

class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        unique_together = ('event', 'email')