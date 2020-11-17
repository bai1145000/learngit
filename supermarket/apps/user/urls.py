from django.contrib import admin
from django.urls import path,include
from .views import UserLogin, UserLogout, RegisterViews
app_name = 'user'

urlpatterns = [
    path('login/', UserLogin.as_view()), #登录
    path('logou/', UserLogout.as_view()), #退出登录
    path('register/', RegisterViews.as_view()) #注册
]