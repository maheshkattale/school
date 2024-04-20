from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', teacher_master.as_view(), name = 'teacher_master'),
    path('add_teacher', add_teacher.as_view(), name = 'add_teacher'),
    path('edit_teacher', edit_teacher.as_view(), name = 'edit_teacher'),
    
    
]