from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #school master
    path('Add', AddSchool.as_view(), name = 'Add'),
    path('list', schoollist.as_view(), name = 'list'),
    path('getbyid', getschoolbyid.as_view(), name = 'getbyid'),
    path('update', updateSchool.as_view(), name = 'update'),
    path('disable', disableSchool.as_view(), name = 'disable'),
    path('enable', enableSchool.as_view(), name = 'enable'),

    #academic year master
    path('AddAcademicYear', AddAcademicYear.as_view(), name = 'AddAcademicYear'),
    path('AcademicYearlist', AcademicYearlist.as_view(), name = 'AcademicYearlist'),
    path('AcademicYearbyid', AcademicYearbyid.as_view(), name = 'AcademicYearbyid'),
    path('updateAcademicYear', updateAcademicYear.as_view(), name = 'updateAcademicYear'),
    path('deleteAcademicYear', deleteAcademicYear.as_view(), name = 'deleteAcademicYear'),
    path('disableAcademicYear', disableAcademicYear.as_view(), name = 'disableAcademicYear'),
    path('enableAcademicYear', enableAcademicYear.as_view(), name = 'enableAcademicYear'),
    path('toggleAcademicYear', toggleAcademicYear.as_view(), name = 'toggleAcademicYear'),
    path('get_current_academic_year', get_current_academic_year.as_view(), name = 'get_current_academic_year'),
    
    
    path('academicdatabyexcel', academicdatabyexcel.as_view(), name = 'academicdatabyexcel'),

    # Announcement master

]