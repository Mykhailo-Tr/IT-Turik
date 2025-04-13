from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_view, name='tasks'),
    path('<int:task_id>/', views.tasks_view, name='task_details'),
    path('create/', views.create_task_view, name='create_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
]