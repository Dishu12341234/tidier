from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('loginUser', views.UserLogin, name='UserLogin'),
    path('logoutUser', views.UserLogout, name='UserLogout'),
    path('POSTDataUpdate', views.POSTDataUpdate, name='POSTDataUpdate'),
    path('addBin', views.addBin, name='addBin'),
]