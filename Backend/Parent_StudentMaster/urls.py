from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddParentStudent.as_view(), name = 'Add'),
    path('list', ParentStudentlist.as_view(), name = 'list'),
    path('getbyid', getParentStudentbyid.as_view(), name = 'getbyid'),
    path('update', updateParentStudent.as_view(), name = 'update'),
    # path('delete', deleteParentStudent.as_view(), name = 'delete'),
    path('studentlist', studentlist.as_view(), name = 'studentlist'),
    path('studentsbyclasslist', studentsbyclasslist.as_view(), name = 'studentsbyclasslist'),
    path('studentsbyparentlist', studentsbyparentlist.as_view(), name = 'studentsbyparentlist'),
    path('bloodgrouplist', bloodgrouplist.as_view(), name = 'bloodgrouplist'),

]