from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', addtimetable.as_view(), name = 'Add'),
    path('getteachersfromsub', getteachersfromsub.as_view(), name = 'getteachersfromsub'),
    path('daterangelist', daterangelist.as_view(), name = 'daterangelist'),
    path('timetablelist', timetablelist.as_view(), name = 'timetablelist'),
    path('checkdaterange', checkdaterange.as_view(), name = 'checkdaterange'),
    path('edittimetable',edittimetable.as_view(), name = 'edittimetable'),
    path('deletetimetable',deletetimetable.as_view(), name = 'deletetimetable'),
    path('get_ttbyid',get_ttbyid.as_view(), name = 'get_ttbyid'),
    path('getttbystudentid',getttbystudentid.as_view(), name = 'getttbystudentid'),
    path('get_recipient',get_recipient.as_view(), name = 'get_recipient'),
    path('get_student_time_table',get_student_time_table.as_view(), name = 'get_student_time_table'),
    path('get_class_time_table',get_class_time_table.as_view(), name = 'get_class_time_table'),
    path('get_teacher_time_table',get_teacher_time_table.as_view(), name = 'get_teacher_time_table'),
    path('timetable_bulk_upload',timetable_bulk_upload.as_view(), name = 'timetable_bulk_upload'),

]