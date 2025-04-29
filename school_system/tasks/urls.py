from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_view, name='tasks'),
    path('<int:task_id>/', views.tasks_view, name='task_details'),
    path('create/', views.create_task_view, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    
    path('tasks/<int:task_id>/toggle-participation/', views.toggle_task_participation, name='toggle_task_participation'),
    path('tasks/<int:task_id>/toggle-completion/', views.toggle_task_completion_view, name='toggle_task_completion'),

]