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
    path('add_class_teacher', add_class_teacher.as_view(), name = 'add_class_teacher'),
    path('get_class_teachers', get_class_teachers.as_view(), name = 'get_class_teachers'),
    path('edit_class_teacher', edit_class_teacher.as_view(), name = 'edit_class_teacher'),
    path('delete_class_teacher', delete_class_teacher.as_view(), name = 'delete_class_teacher'),

]