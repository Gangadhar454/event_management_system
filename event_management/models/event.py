from django.db import models
import pendulum

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')

    def save(self, *args, **kwargs):
        if self.timezone:
            tz = pendulum.timezone(self.timezone)
            self.start_time = pendulum.instance(self.start_time).in_timezone(tz).astimezone(pendulum.timezone('UTC'))
            self.end_time = pendulum.instance(self.end_time).in_timezone(tz).astimezone(pendulum.timezone('UTC'))
        super().save(*args, **kwargs)

    def get_start_time_in_timezone(self, tz_name):
        return pendulum.instance(self.start_time).astimezone(pendulum.timezone(tz_name))

    def get_end_time_in_timezone(self, tz_name):
        return pendulum.instance(self.end_time).astimezone(pendulum.timezone(tz_name))