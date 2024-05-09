from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', exam.as_view(), name = 'exam'),
    path('edit_exam/<str:id>', edit_exam.as_view(), name = 'edit_exam'),
    path('add_exam', add_exam.as_view(), name = 'add_exam'),
    path('exam_type', exam_type.as_view(), name = 'exam_type'),
    path('add_exam_type', add_exam_type.as_view(), name = 'add_exam_type'),
    path('edit_exam_type', edit_exam_type.as_view(), name = 'edit_exam_type'),
    path('delete_exam_type', delete_exam_type.as_view(), name = 'delete_exam_type'),
    path('delete_exam', delete_exam.as_view(), name = 'delete_exam'),
    
    
]