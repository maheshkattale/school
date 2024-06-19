from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('profile', profile.as_view(), name = 'profile'),
    path('reset_password/<str:id>', reset_password.as_view(), name = 'reset_password'),
    path('forgot_password', forgot_password.as_view(), name = 'forgot_password'),
    path('change_password/<str:id>', change_password.as_view(), name = 'change_password'),
    path('set_password/<str:id>', set_password.as_view(), name = 'set_password'),
    path('permissions', permissions.as_view(), name = 'permissions'),
    path('get_permissions_by_role', get_permissions_by_role.as_view(), name = 'get_permissions_by_role'),
    path('update_profile', update_profile.as_view(), name = 'update_profile'),
    
    
]