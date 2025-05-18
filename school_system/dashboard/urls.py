from django.urls import path
from .views import accounts_views
from .views.subjects_views import add_subject_ajax, remove_subject_ajax
from .views.children_views import add_child_ajax, remove_child_ajax
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
    
    path('ajax/add-child/', add_child_ajax, name='add_child_ajax'),
    path('ajax/remove-child/', remove_child_ajax, name='remove_child_ajax'),
    path('ajax/add-subject/', add_subject_ajax, name='add_subject_ajax'),
    path('ajax/remove-subject/', remove_subject_ajax, name='remove_subject_ajax'),
]