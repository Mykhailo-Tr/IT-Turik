from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_view, name='tasks'),
    path('<int:task_id>/', views.tasks_view, name='task_details'),
    path('create/', views.create_task_view, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    
    path('take/<int:task_id>/', views.take_task_view, name='take_task'),
    path('complete/<int:task_id>/', views.complete_task_view, name='complete_task'),
    path('uncomplete/<int:task_id>/', views.uncomplete_task_view, name='uncomplete_task'),
]