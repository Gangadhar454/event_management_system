from rest_framework import serializers
from event_management.models.event import Event
import pendulum

class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S %Z')
    timezone = serializers.CharField(required=False, default='Asia/Kolkata')

    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'start_time', 'end_time', 'max_capacity', 'timezone']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        if data['max_capacity'] <= 0:
            raise serializers.ValidationError("Max capacity must be positive")
        try:
            pendulum.timezone(data.get('timezone', 'Asia/Kolkata'))
        except pendulum.exceptions.PendulumException:
            raise serializers.ValidationError("Invalid timezone")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tz = pendulum.timezone(instance.timezone)
        representation['start_time'] = instance.get_start_time_in_timezone(tz.name).strftime('%Y-%m-%d %H:%M:%S %Z')
        representation['end_time'] = instance.get_end_time_in_timezone(tz.name).strftime('%Y-%m-%d %H:%M:%S %Z')
        return representation