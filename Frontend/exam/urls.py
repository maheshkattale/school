from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', exam.as_view(), name = 'exam'),
    path('edit_exam/<str:id>', edit_exam.as_view(), name = 'edit_exam'),
    path('add_exam', add_exam.as_view(), name = 'add_exam'),
    path('delete_exam', delete_exam.as_view(), name = 'delete_exam'),
    path('get_marks_by_exam_type', get_marks_by_exam_type.as_view(), name = 'get_marks_by_exam_type'),

    
    path('exam_type', exam_type.as_view(), name = 'exam_type'),
    path('add_exam_type_marks', add_exam_type_marks.as_view(), name = 'add_exam_type_marks'),
    path('edit_exam_type_marks', edit_exam_type_marks.as_view(), name = 'edit_exam_type_marks'),
    path('delete_exam_type_marks', delete_exam_type_marks.as_view(), name = 'delete_exam_type_marks'),
    
    
]