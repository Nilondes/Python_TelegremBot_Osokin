from rest_framework import serializers
from calender.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'end_time']
