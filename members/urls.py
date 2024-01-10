from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

urlpatterns = [
    path("", views.members, name="members"),
    path("loginUser", views.UserLogin, name="UserLogin"),
    path("logoutUser", views.UserLogout, name="UserLogout"),
    path("creatBin", views.creatBin, name="creatBin"),
    path("update", views.update, name="update"),
    path("QR", views.genQRCODE, name="QR"),
    path("connect", views.connect, name="connect"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.png")),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
