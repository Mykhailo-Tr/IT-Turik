from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.RegisterView.as_view(), name='register'),
    path('singup/student/', views.StudentSignUpView.as_view(), name='register_student'),
    path('signup/teacher/', views.TeacherSignUpView.as_view(), name='register_teacher'),
    path('signup/parent/', views.ParentSignUpView.as_view(), name='register_parent'),
    
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/edit/', views.edit_account_view, name='edit_account'),
    path('account/delete/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/delete-photo/', views.delete_profile_photo_view, name='delete_profile_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)