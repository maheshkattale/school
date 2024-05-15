from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddClass.as_view(), name = 'Add'),
    path('List', classlist.as_view(), name = 'list'),
    path('getbyid',getclassbyid.as_view(), name = 'getbyid'),
    path('update', updateclass.as_view(), name = 'update'),
    path('delete', deleteclass.as_view(), name = 'delete'),

    path('classdatabyexcel', classdatabyexcel.as_view(), name = 'classdatabyexcel'),

]