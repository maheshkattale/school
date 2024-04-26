from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', parent_student_master.as_view(), name = 'parent_student_master'),
    path('add_parent_student', add_parent_student.as_view(), name = 'add_parent_student'),
    path('edit_parent_student/<str:id>', edit_parent_student.as_view(), name = 'edit_parent_student'),
    path('student_list', student_list.as_view(), name = 'student_list'),
    path('delete_parent', delete_parent.as_view(), name = 'delete_parent'),
    path('delete_student', delete_student.as_view(), name = 'delete_student'),
    
]