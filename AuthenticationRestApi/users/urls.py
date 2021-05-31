from django.urls import path, include
from users import views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', views.RegisterView.as_view()),
    path('api/auth/login', views.LoginView.as_view()),
    path('changePassword', views.ChangePasswordView.as_view()),
]
