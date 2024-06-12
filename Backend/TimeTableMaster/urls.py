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
    path('get_time_table',get_time_table.as_view(), name = 'get_time_table'),

]