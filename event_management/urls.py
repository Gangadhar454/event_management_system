from django.urls import path
from event_management.views import event_views, attendee_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version='v1',
        description="API for managing events and attendees",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('events/', event_views.EventCreateListView.as_view(), name='event-create-list'),
    path('events/<str:event_id>/register/', attendee_views.RegisterAttendeeView.as_view(), name='register-attendee'),
    path('events/<str:event_id>/attendees/', attendee_views.EventAttendeesView.as_view(), name='event-attendees'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)