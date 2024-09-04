from django.shortcuts import render
from rest_framework import generics
from api.serializers import EventSerializer
from calender.models import Event, PublicEvents

public_events = PublicEvents.objects.filter(status='public').values('event_id')

class EventView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(id__in=public_events)
