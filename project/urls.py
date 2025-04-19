from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('drones.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


from django.contrib.auth import views as auth_views

urlpatterns += [
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

from app import views as app_views

urlpatterns += [
    path('accounts/register/', app_views.register, name='register'),
    path('accounts/activate/<uidb64>/<token>/', app_views.activate, name='activate'),
]
handler403 = 'your_app.views.permission_denied_view'
handler404 = 'your_app.views.custom_404_view'
handler500 = 'your_app.views.custom_500_view'
