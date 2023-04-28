from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth'

urlpatterns = [
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]




