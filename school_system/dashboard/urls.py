from django.urls import path

from accounts.views import edit_profile_view, delete_profile_photo_view
from .views import accounts_views
from .views.subjects_views import subjects_view, attach_subject_view, detach_subject_view, delete_subject_view
from .views.children_views import children_view

urlpatterns = [
    path('', accounts_views.dashboard_view, name='dashboard'),
    path('accounts/', accounts_views.accounts_view, name='dashboard_accounts'),
    path('accounts/create/<str:role>/', accounts_views.create_account_view, name='dashboard_create_account'),
    path('accounts/<int:user_id>/edit/', accounts_views.edit_account_view, name='dashboard_edit_account'),
    path('accounts/<int:user_id>/profile/edit/', edit_profile_view, name='dashboard_edit_profile'),
    path('accounts/<int:user_id>/profile/delete-photo/', delete_profile_photo_view, name='dashboard_delete_profile_photo'),
    path('accounts/<int:user_id>/delete/', accounts_views.delete_account_view, name='dashboard_delete_account'),
    path('accounts/profile/<int:user_id>/', accounts_views.profile_view, name='dashboard_profile'),
    
    path('subjects/', subjects_view, name='dashboard_subjects'),
    path('subjects/attach/<int:subject_id>/', attach_subject_view, name='attach_subject'),
    path('subjects/detach/<int:subject_id>/', detach_subject_view, name='detach_subject'),
    path('subjects/delete/<int:subject_id>/', delete_subject_view, name='delete_subject'),


    path('children/', children_view, name='dashboard_children'),
]