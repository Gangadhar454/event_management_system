from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from event_management.serializers.attendee_serializer import AttendeeSerializer
from event_management.services.event_service import EventService

class RegisterAttendeeView(generics.GenericAPIView):
    serializer_class = AttendeeSerializer

    def post(self, request, event_id, *args, **kwargs):
        """Register an attendee for an event."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                attendee = EventService.register_attendee(event_id, serializer.validated_data)
                return Response(AttendeeSerializer(attendee).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventAttendeesView(generics.GenericAPIView):
    serializer_class = AttendeeSerializer
    pagination_class = PageNumberPagination

    def get(self, request, event_id, *args, **kwargs):
        """List all attendees for an event with pagination."""
        attendees = EventService.get_event_attendees(event_id, request.query_params.get('page'), self.pagination_class.page_size)
        page = self.paginate_queryset(attendees)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(attendees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)