from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddDesignation.as_view(), name = 'Add'),
    path('List', Designationlist.as_view(), name = 'list'),
    path('getbyid',getDesignationbyid.as_view(), name = 'getbyid'),
    path('update', updatedesignation.as_view(), name = 'update'),
    path('delete', deletedesignation.as_view(), name = 'delete'),
    path('designationdatabyexcel', designationdatabyexcel.as_view(), name = 'designationdatabyexcel'),

]