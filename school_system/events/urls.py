from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_view, name='events'),
    path('<int:event_id>/', views.events_view, name="event_details"),
    path('create/', views.create_event_view, name="create_event"),
    path('edit/<int:event_id>/', views.edit_event_view, name="edit_event"),
    path('delete/<int:event_id>/', views.delete_event_view, name="delete_event"),
    path('respond/<int:event_id>/<str:response>/', views.respond_to_event, name='respond_to_event'),
    path('leave/<int:event_id>/', views.leave_event_view, name='leave_event'),
    path('<int:event_id>/comment/', views.add_event_comment, name='add_event_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_event_comment, name='delete_event_comment'),


]