from django.contrib import admin
from .models import Event, BotStatistics, Appointment, User


admin.site.register(Event)
admin.site.register(BotStatistics)
admin.site.register(Appointment)
admin.site.register(User)
