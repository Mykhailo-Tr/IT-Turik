from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_view, name='events'),
    path('<int:event_id>', views.events_view, name="event_details"),
    path('create/', views.create_event_view, name="create_event"),
    path('edit/<int:event_id>', views.edit_event_view, name="edit_event"),
    path('delete/<int:event_id>', views.delete_event_view, name="delete_event"),
]