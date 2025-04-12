from django.urls import path, include
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
    path('account/edit/', views.edit_account_view, name='edit_account'),
    path('account/delete/', views.delete_account_view, name='delete_account'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
