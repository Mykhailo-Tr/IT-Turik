from django.urls import path
from .views import (
    EventListView, EventCreateView, EventEditView, EventDeleteView,
    RespondToEventView, LeaveEventView, EventCommentAddView, EventCommentDeleteView
)

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
    path('<int:event_id>/', EventListView.as_view(), name="event_details"),
    path('create/', EventCreateView.as_view(), name="create_event"),
    path('edit/<int:event_id>/', EventEditView.as_view(), name="edit_event"),
    path('delete/<int:event_id>/', EventDeleteView.as_view(), name="delete_event"),
    path('respond/<int:event_id>/<str:response>/', RespondToEventView.as_view(), name='respond_to_event'),
    path('leave/<int:event_id>/', LeaveEventView.as_view(), name='leave_event'),
    path('<int:event_id>/comment/', EventCommentAddView.as_view(), name='add_event_comment'),
    path('comment/<int:comment_id>/delete/', EventCommentDeleteView.as_view(), name='delete_event_comment'),
]
