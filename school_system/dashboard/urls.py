from django.urls import path

from accounts import views as accounts_views
from .views import dashboard_views
from .views.subjects_views import subjects_view, attach_subject_view, detach_subject_view, delete_subject_view
from .views.children_views import children_view

urlpatterns = [
    path('', dashboard_views.dashboard_view, name='dashboard'),
    path('accounts/', dashboard_views.accounts_view, name='dashboard_accounts'),
    
    path('accounts/<int:user_id>/', accounts_views.AccountView.as_view(), name='account'),
    path('accounts/create/<str:role>/', dashboard_views.create_account_view, name='create_account'),
    path('accounts/<int:user_id>/edit/', accounts_views.edit_account_view, name='edit_account'),
    path('accounts/<int:user_id>/delete/', accounts_views.DeleteAccountView.as_view(), name='delete_account'),
    
    path('profile/<int:user_id>/', accounts_views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/edit/', accounts_views.edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/delete-photo/', accounts_views.delete_profile_photo_view, name='delete_profile_photo'),
    
    path('subjects/', subjects_view, name='dashboard_subjects'),
    path('subjects/attach/<int:subject_id>/', attach_subject_view, name='attach_subject'),
    path('subjects/detach/<int:subject_id>/', detach_subject_view, name='detach_subject'),
    path('subjects/delete/<int:subject_id>/', delete_subject_view, name='delete_subject'),

    path('children/', children_view, name='dashboard_children'),
]