"""authenticationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')) 
"""

from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from dogApp import views

urlpatterns = [
    path('adduser/', views.UserCreateView.as_view()),
    path('loginUser/', TokenObtainPairView.as_view()),
    path('refreshToken/', TokenRefreshView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view()),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view()),
    path('user/list/', views.UserList.as_view()),
    path('api/dogs/', views.DogList.as_view()),
    path('api/dogs/<str:name>/', views.DogDetailView.as_view()),
    path('api/dogs/is_adopted', views.DogFilterListView.as_view()),
    path('api/dogs/name', views.DogCreateView.as_view()),
    path('api/dogs/<str:name>', views.DogUpdateView.as_view()),
    path('api/dog/<str:name>', views.DogDeleteView.as_view()),
]