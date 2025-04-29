from django.urls import path
from . import views
from accounts.views import edit_profile_view, delete_profile_photo_view

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('accounts/', views.accounts_view, name='dashboard_accounts'),
    path('accounts/create/<str:role>/', views.create_account_view, name='dashboard_create_account'),
    path('accounts/<int:user_id>/edit/', views.edit_account_view, name='dashboard_edit_account'),
    path('accounts/<int:user_id>/profile/edit/', edit_profile_view, name='dashboard_edit_profile'),
    path('accounts/<int:user_id>/profile/delete-photo/', delete_profile_photo_view, name='dashboard_delete_profile_photo'),
    path('accounts/<int:user_id>/delete/', views.delete_account_view, name='dashboard_delete_account'),
    
    path('profile/<int:user_id>/', views.profile_view, name='dashboard_profile'),
]