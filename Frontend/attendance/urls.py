from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('class_attendance', class_attendance.as_view(), name = 'class_attendance'),

    
]