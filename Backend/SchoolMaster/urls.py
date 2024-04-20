from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddSchool.as_view(), name = 'Add'),
    path('list', schoollist.as_view(), name = 'list'),
    path('getbyid', getschoolbyid.as_view(), name = 'getbyid'),
    path('update', updateSchool.as_view(), name = 'update'),
    path('disable', disableSchool.as_view(), name = 'disable'),
    path('enable', enableSchool.as_view(), name = 'enable'),
]