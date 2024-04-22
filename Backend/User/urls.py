from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login.as_view(), name = 'login'),
    path('logout', logout.as_view(), name = 'logout'),
    path('userlist', Userlist.as_view(), name = 'Userlist'),
    path('getpermissions', getpermissions.as_view(), name = 'getpermissions'),
    path('savepermissions', savepermissions.as_view(), name = 'savepermissions'),
]