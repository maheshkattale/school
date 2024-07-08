from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', time_table_master.as_view(), name = 'time_table_master'),
    path('add_time_table', add_time_table.as_view(), name = 'add_time_table'),
    path('edit_timetable', edit_timetable.as_view(), name = 'edit_timetable'),
    path('delete_timetable', delete_timetable.as_view(), name = 'delete_timetable'),
    path('get_timetable_by_id', get_timetable_by_id.as_view(), name = 'get_timetable_by_id'),
    path('get_teacher_by_subject', get_teacher_by_subject.as_view(), name = 'get_teacher_by_subject'),
    path('time_table_list', time_table_list.as_view(), name = 'time_table_list'),
    path('check_existing_timetable_entry', check_existing_timetable_entry.as_view(), name = 'check_existing_timetable_entry'),
    
    path('get_student_time_table', get_student_time_table.as_view(), name = 'get_student_time_table'),
    path('get_class_time_table', get_class_time_table.as_view(), name = 'get_class_time_table'),
    path('get_teacher_time_table', get_teacher_time_table.as_view(), name = 'get_teacher_time_table'),
    path('timetable_bulk_upload', timetable_bulk_upload.as_view(), name = 'timetable_bulk_upload'),
    
]