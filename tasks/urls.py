from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    ToggleTaskParticipationView, ToggleTaskCompletionView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_details'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='edit_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),

    path('tasks/<int:task_id>/toggle-participation/', ToggleTaskParticipationView.as_view(), name='toggle_task_participation'),
    path('tasks/<int:task_id>/toggle-completion/', ToggleTaskCompletionView.as_view(), name='toggle_task_completion'),
]
