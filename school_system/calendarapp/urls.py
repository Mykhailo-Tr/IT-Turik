from django.urls import path
from .views import (
    FullCalendarView,
    EventListJsonView,
    CreateEventView,
    UpdateEventDateView,
    DeleteEventView,
    EventFormPartialView,
)

app_name = 'calendarapp'

urlpatterns = [
    path('', FullCalendarView.as_view(), name='calendar'),
    path('events/json/', EventListJsonView.as_view(), name='events_json'),
    path('events/create/', CreateEventView.as_view(), name='create_event'),
    path('events/create/form/', EventFormPartialView.as_view(), name='create_event_form'),
    path('events/update/<int:event_id>/', UpdateEventDateView.as_view(), name='update_event_date'),
    path('events/delete/<int:event_id>/', DeleteEventView.as_view(), name='delete_event'),
]
