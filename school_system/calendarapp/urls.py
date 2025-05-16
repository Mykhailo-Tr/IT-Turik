# calendarapp/urls.py
from django.urls import path
from .views import FullCalendarView, get_events_json, create_event, update_event_date, delete_event

app_name = 'calendarapp'

urlpatterns = [
    path('', FullCalendarView.as_view(), name='calendar'),
    path('events/json/', get_events_json, name='events_json'),
    path('events/create/', create_event, name='create_event'),
    path('events/update/<int:event_id>/', update_event_date, name='update_event_date'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
]
