from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [

  path('register/', register, name="register"),
  path('logout/', logout, name="logout"),
  path('login/', loginView, name="login"), 

  path('profile/', pilot_profile, name='pilot_profile'),
  path('profile/training/<int:pk>/delete/', delete_training, name='delete_training'),

  path('test-login/', test_login, name='test_login'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



