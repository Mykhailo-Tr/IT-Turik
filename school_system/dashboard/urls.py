from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('accounts/', views.accounts_view, name='teacher_accounts'),
    path('accounts/create/<str:role>/', views.create_account_view, name='teacher_create_account'),
    path('accounts/<int:user_id>/edit/', views.edit_account_view, name='teacher_edit_account'),
    path('accounts/<int:user_id>/profile/edit/', views.edit_profile_view, name='teacher_edit_profile'),
    path('accounts/<int:user_id>/delete/', views.delete_account_view, name='teacher_delete_account'),
]