from rest_framework import generics, status
from rest_framework.response import Response
from event_management.models.event import Event
from event_management.serializers.event_serializer import EventSerializer
from event_management.services.event_service import EventService

class EventCreateListView(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def post(self, request, *args, **kwargs):
        """Create a new event."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = EventService.create_event(serializer.validated_data)
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """List all upcoming events."""
        events = EventService.get_upcoming_events()
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)