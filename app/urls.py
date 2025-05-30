from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [

  path('register/', register, name="register"),
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



  path('profile/', pilot_profile, name='pilot_profile'),
  path('profile/training/<int:pk>/delete/', delete_training, name='delete_training'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



