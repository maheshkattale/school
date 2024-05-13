from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', academic_master.as_view(), name = 'academic_master'),
    path('edit_academic', edit_academic.as_view(), name = 'edit_academic'),
    path('delete_academic', delete_academic.as_view(), name = 'delete_academic'),
    path('toggleAcademicYear', toggleAcademicYear.as_view(), name = 'toggleAcademicYear'),
 
    path('enableAcademicYear', enableAcademicYear.as_view(), name = 'enableAcademicYear'),
    
    
]