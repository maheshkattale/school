from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', exam.as_view(), name = 'exam'),
    path('edit_exam', edit_exam.as_view(), name = 'edit_exam'),
    path('add_exam', add_exam.as_view(), name = 'add_exam'),
    path('exam_type', exam_type.as_view(), name = 'exam_type'),
    
    
]