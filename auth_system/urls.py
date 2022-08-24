from django.urls import path
from auth_system.views import (send_email,
    activate_account,home,Register,
    change_password_online,
    password_reset,
    forget_passowrd)
from rest_framework.authtoken.views import obtain_auth_token

# app_name='user'

urlpatterns = [
    # path('send/',send_email,name='send-email'),
    path('activate/<uuid:uuid>/',activate_account,name='activate-account'),
    # path('',home,name='home'),
    path('api/user/register/',Register.as_view(),name='register'),
    path('api/user/forget-password/',forget_passowrd,name='forget_password'),
    path('user/online/passwordchange/',change_password_online,name='change-online-password'),
    path('api/user/login/',obtain_auth_token,name='login'),
    path('api/user/password/reset/',password_reset,name='password-reset')
]
