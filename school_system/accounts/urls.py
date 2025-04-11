from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register_view, name='register'),
    path('singup/student/', views.StudentSignUpView.as_view(), name='register_student'),
    path('signup/teacher/', views.TeacherSignUpView.as_view(), name='register_teacher'),
    path('signup/parent/', views.ParentSignUpView.as_view(), name='register_parent'),
    path('account/', views.account_view, name='account'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='view_profile'),
    path('edit-account/', views.edit_account_view, name='edit_account'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/teacher/accounts/', views.teacher_accounts_view, name='teacher_accounts'),
    path('dashboard/teacher/create/<str:role>/', views.teacher_create_account_view, name='teacher_create_account'),
    path('dashboard/teacher/account/<int:user_id>/edit/', views.edit_account_view, name='teacher_edit_account'),
    path('dashboard/teacher/profile/<int:user_id>/edit/', views.edit_profile_view, name='teacher_edit_profile'),
    path('dashboard/teacher/account/<int:user_id>/delete/', views.teacher_delete_account_view, name='teacher_delete_account'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
