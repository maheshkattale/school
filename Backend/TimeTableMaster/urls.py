from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', addtimetable.as_view(), name = 'Add'),
    path('getteachersfromsub', getteachersfromsub.as_view(), name = 'getteachersfromsub'),
    path('daterangelist', daterangelist.as_view(), name = 'daterangelist'),
    path('timetablelist', timetablelist.as_view(), name = 'timetablelist'),

   

]