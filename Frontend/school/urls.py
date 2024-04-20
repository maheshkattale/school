from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', login.as_view(), name = 'login'),
    path('dashboard', dashboard.as_view(), name = 'dashboard'),
    path('school_master', school_master.as_view(), name = 'school_master'),
    path('add_school', add_school.as_view(), name = 'add_school'),
    path('edit_school', edit_school.as_view(), name = 'edit_school'),
    
    
]