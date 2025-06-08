from django.db import transaction
from django.core.exceptions import ValidationError
from event_management.models.event import Event
from event_management.models.attendee import Attendee
import pendulum
from rest_framework.exceptions import APIException

class EventService:
    @staticmethod
    def create_event(data):
        try:
            with transaction.atomic():
                event = Event.objects.create(**data)
                return event
        except Exception as e:
            raise APIException(f"Failed to create event: {str(e)}")

    @staticmethod
    def get_upcoming_events():
        now = pendulum.now('UTC')
        return Event.objects.filter(start_time__gte=now).order_by('start_time')

    @staticmethod
    def register_attendee(event_id, attendee_data):
        try:
            with transaction.atomic():
                event = Event.objects.get(id=event_id)
                if event.attendees.count() >= event.max_capacity:
                    raise ValidationError("Event is at full capacity")
                if event.attendees.filter(email=attendee_data['email']).exists():
                    raise ValidationError("Email already registered for this event")
                attendee = Attendee.objects.create(event=event, **attendee_data)
                return attendee
        except Event.DoesNotExist:
            raise APIException("Event not found")
        except Exception as e:
            raise APIException(f"Failed to register attendee: {str(e)}")

    @staticmethod
    def get_event_attendees(event_id, page, page_size):
        try:
            event = Event.objects.get(id=event_id)
            return event.attendees.all()
        except Event.DoesNotExist:
            raise APIException("Event not found")