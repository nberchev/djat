from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from personal.views import home_screen_view

from accounts.views import register_user, login_user, logout_user

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', home_screen_view, name='home'),

                  path('register/', register_user, name='register'),
                  path('login/', login_user, name='login'),
                  path('logout/', logout_user, name='logout'),

                  path('password_change/',
                       auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
                       name='password_change'),
                  path('password_change/done/',
                       auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
                       name='password_change_done'),

                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

                  path('account/', include('accounts.urls', namespace='account')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
