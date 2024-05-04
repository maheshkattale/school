from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #examtypemaster
    path('Add', AddExamType.as_view(), name = 'Add'),
    path('List', ExamTypelist.as_view(), name = 'list'),
    path('getbyid',ExamTypebyid.as_view(), name = 'getbyid'),
    path('update', updateExamType.as_view(), name = 'update'),
    path('delete', deleteExamType.as_view(), name = 'delete'),

    #exammaster
    path('AddExam', AddExam.as_view(), name = 'AddExam'),
    path('Examlist', Examlist.as_view(), name = 'Examlist'),
    path('Exambyid', Exambyid.as_view(), name = 'Exambyid'),
    path('updateexam', updateexam.as_view(), name = 'updateexam'),
    path('deleteexam', deleteexam.as_view(), name = 'deleteexam'),


    path('uploadmarksheet', uploadmarksheet.as_view(), name = 'uploadmarksheet'),



]