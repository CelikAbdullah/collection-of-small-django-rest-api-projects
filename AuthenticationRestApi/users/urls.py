from django.urls import path, include
from users import views
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', views.RegisterView.as_view()),
    path('api/auth/login', views.LoginView.as_view()),
    path('changePassword', views.ChangePasswordView.as_view()),
    path('logout', knox_views.LogoutView.as_view()),
]
