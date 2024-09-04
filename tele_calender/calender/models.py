from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=40, unique=True)
    chat_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.user_name}"



class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(default='00:00:00')
    event_details = models.TextField()
    chat = models.ForeignKey(User, to_field='chat_id', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"


class BotStatistics(models.Model):
    date = models.DateField()
    user_count = models.PositiveIntegerField()
    event_count = models.PositiveIntegerField()
    edited_events = models.PositiveIntegerField()
    cancelled_events = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date}"


class Appointment(models.Model):
    statuses = {"confirmed": "confirmed", "awaiting": "awaiting", "declined":"declined"}
    user = models.ForeignKey(User, to_field='user_name', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(default='00:00:00')
    details = models.TextField(blank=True)
    status = models.CharField(max_length=40, choices=statuses)

    def __str__(self):
        return f"{self.user} - {self.event.name} - {self.date} - {self.time} - {self.status}"

class PublicEvents(models.Model):
    public = {'public': 'public', 'private': 'private'}
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=public)

    def __str__(self):
        return f'{self.event.primary_key} - {self.status}'