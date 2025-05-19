from django.urls import path

from accounts import views as accounts_views
from .views import dashboard_views
from .views.subjects_views import SubjectsView, AttachSubjectView, DetachSubjectView, DeleteSubjectView
from .views.children_views import ChildrenView

urlpatterns = [
    path('', dashboard_views.DashboardView.as_view(), name='dashboard'),
    path('accounts/', dashboard_views.AccountsView.as_view(), name='dashboard_accounts'),
    
    path('accounts/<int:user_id>/', accounts_views.AccountView.as_view(), name='account'),
    path('accounts/create/<str:role>/', dashboard_views.CreateAccountView.as_view(), name='create_account'),
    path('accounts/<int:user_id>/edit/', accounts_views.AccountUpdateView.as_view(), name='edit_account'),
    path('accounts/<int:user_id>/delete/', accounts_views.DeleteAccountView.as_view(), name='delete_account'),
    
    path('profile/<int:user_id>/', accounts_views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/edit/', accounts_views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<int:user_id>/delete-photo/', accounts_views.DeleteProfilePhotoView.as_view(), name='delete_profile_photo'),
    
    path('subjects/', SubjectsView.as_view(), name='dashboard_subjects'),
    path('subjects/attach/<int:subject_id>/', AttachSubjectView.as_view(), name='attach_subject'),
    path('subjects/detach/<int:subject_id>/', DetachSubjectView.as_view(), name='detach_subject'),
    path('subjects/delete/<int:subject_id>/', DeleteSubjectView.as_view(), name='delete_subject'),

    path('children/', ChildrenView.as_view(), name='dashboard_children'),
]