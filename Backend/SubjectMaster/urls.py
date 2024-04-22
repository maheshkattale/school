from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddSubject.as_view(), name = 'Add'),
    path('List', Subjectlist.as_view(), name = 'list'),
    path('getbyid',getSubjectbyid.as_view(), name = 'getbyid'),
    path('update', updateSubject.as_view(), name = 'update'),
    path('delete', deleteSubject.as_view(), name = 'delete'),

]