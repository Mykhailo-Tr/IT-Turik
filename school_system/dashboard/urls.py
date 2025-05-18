from django.urls import path
from .views import accounts_views
from accounts.views import edit_profile_view, delete_profile_photo_view

urlpatterns = [
    path('', accounts_views.dashboard_view, name='dashboard'),
    path('accounts/', accounts_views.accounts_view, name='dashboard_accounts'),
    path('accounts/create/<str:role>/', accounts_views.create_account_view, name='dashboard_create_account'),
    path('accounts/<int:user_id>/edit/', accounts_views.edit_account_view, name='dashboard_edit_account'),
    path('accounts/<int:user_id>/profile/edit/', edit_profile_view, name='dashboard_edit_profile'),
    path('accounts/<int:user_id>/profile/delete-photo/', delete_profile_photo_view, name='dashboard_delete_profile_photo'),
    path('accounts/<int:user_id>/delete/', accounts_views.delete_account_view, name='dashboard_delete_account'),
    path('accounts/profile/<int:user_id>/', accounts_views.profile_view, name='dashboard_profile'),
]