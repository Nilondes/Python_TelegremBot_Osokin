import csv
from .models import Event
from django.http import HttpResponse


def user_events(request, chat_id):
    events = Event.objects.get_queryset().filter(chat_id=chat_id).values()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="user_events.csv"'},
    )
    writer = csv.DictWriter(response, fieldnames=['id', 'name', 'date', 'time', 'end_time', 'event_details', 'chat_id'])
    for event in events:
        writer.writerow(event)
    return response
