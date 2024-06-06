from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('class_attendance', class_attendance.as_view(), name = 'class_attendance'),
    path('get_class_attendance_by_date', get_class_attendance_by_date.as_view(), name = 'get_class_attendance_by_date'),
    path('mark_class_attendance', mark_class_attendance.as_view(), name = 'mark_class_attendance'),

    
]