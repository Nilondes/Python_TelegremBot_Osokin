from django.urls import path
from api.views import EventView

urlpatterns = [
    path('events/', EventView.as_view())
]