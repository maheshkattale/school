from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('profile', profile.as_view(), name = 'profile'),
    path('reset_password', reset_password.as_view(), name = 'reset_password'),
    path('set_password', set_password.as_view(), name = 'set_password'),

    
]