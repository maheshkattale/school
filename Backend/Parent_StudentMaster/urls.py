from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddParentStudent.as_view(), name = 'Add'),
    path('list', ParentStudentlist.as_view(), name = 'list'),
    path('getbyid', getParentStudentbyid.as_view(), name = 'getbyid'),
    path('update', updateParentStudent.as_view(), name = 'update'),
    path('delete', deleteParent.as_view(), name = 'delete'),

    path('studentlist', studentlist.as_view(), name = 'studentlist'),
    path('studentsbyclasslist', studentsbyclasslist.as_view(), name = 'studentsbyclasslist'),
    path('studentsbyparentlist', studentsbyparentlist.as_view(), name = 'studentsbyparentlist'),
    path('bloodgrouplist', bloodgrouplist.as_view(), name = 'bloodgrouplist'),
    path('deleteStudent', deleteStudent.as_view(), name = 'deleteStudent'),

    path('getstudentlist', getstudentlist.as_view(), name = 'getstudentlist'),
    path('getstudentidcards', getstudentidcards.as_view(), name = 'getstudentidcards'),

    #announcements
    path('addannouncement', addannouncement.as_view(), name = 'addannouncement'),
]