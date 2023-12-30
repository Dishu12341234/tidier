from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('members.urls')),
    path("divyansh/", admin.site.urls),
]
