from rest_framework import serializers
from event_management.models.attendee import Attendee

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email']