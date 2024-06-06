from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', class_master.as_view(), name = 'class_master'),
    path('add_class', add_class.as_view(), name = 'add_class'),
    path('edit_class', edit_class.as_view(), name = 'edit_class'),
    path('delete_class', delete_class.as_view(), name = 'delete_class'),

    # class_teachers
    path('class_teachers', class_teachers.as_view(), name = 'class_teachers'),
    path('add_class_teacher', add_class_teacher.as_view(), name = 'add_class_teacher'),
    path('delete_class_teacher', delete_class_teacher.as_view(), name = 'delete_class_teacher'),
    path('edit_class_teacher', edit_class_teacher.as_view(), name = 'edit_class_teacher'),
    
]