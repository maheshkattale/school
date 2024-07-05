from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddTeacher.as_view(), name = 'Add'),
    path('list', Teacherlist.as_view(), name = 'list'),
    path('getbyid', getTeacherbyid.as_view(), name = 'getbyid'),
    path('update', UpdateTeacher.as_view(), name = 'list'),
    path('delete', deleteTeacher.as_view(), name = 'list'),
    
    path('teacherdatabyexcel', teacherdatabyexcel.as_view(), name = 'teacherdatabyexcel'),

]