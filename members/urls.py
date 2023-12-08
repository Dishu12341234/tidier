from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('loginUser', views.UserLogin, name='UserLogin'),
    path('logoutUser', views.UserLogout, name='UserLogout'),
    path('addBin', views.addBin, name='addBin'),
    path('update', views.update, name='update'),
]