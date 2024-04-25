from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('profile', profile.as_view(), name = 'profile'),
    path('reset_password/<str:id>', reset_password.as_view(), name = 'reset_password'),
    path('forgot_password', forgot_password.as_view(), name = 'forgot_password'),
    path('set_password/<str:id>', set_password.as_view(), name = 'set_password'),

    
]