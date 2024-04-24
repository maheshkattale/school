from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', teacher_master.as_view(), name = 'teacher_master'),
    path('add_teacher', add_teacher.as_view(), name = 'add_teacher'),
    path('edit_teacher/<str:id>', edit_teacher.as_view(), name = 'edit_teacher'),
    path('delete_teacher', delete_teacher.as_view(), name = 'delete_teacher'),
    
    
]