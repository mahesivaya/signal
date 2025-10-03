from django.urls import path, include
from . import views
from .models import User

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginView, name='login'),
    path('home', views.home, name='home'),
    path('userpage/<str:username>', views.userpage, name='userpage'),
    path('logout', views.logout, name='logout'),
    path('forgot-password', views.forgotPassword, name='forgot-password'),
]
