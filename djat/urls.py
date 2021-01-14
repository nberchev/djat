from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from personal.views import home_screen_view

from accounts.views import register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('register/', register_user, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
