from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register_view, name='register'),
    path('singup/student/', views.StudentSignUpView.as_view(), name='register_student'),
    path('signup/teacher/', views.TeacherSignUpView.as_view(), name='register_teacher'),
    path('signup/parent/', views.ParentSignUpView.as_view(), name='register_parent'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('dashboard/teacher/create/<str:role>/', views.teacher_create_account_view, name='teacher_create_account'),
    path('dashboard/teacher/<int:user_id>/delete/', views.teacher_delete_account_view, name='teacher_delete_account'),

]
