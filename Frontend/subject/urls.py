from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', subject_master.as_view(), name = 'subject_master'),
    path('add_subject', add_subject.as_view(), name = 'add_subject'),
    path('edit_subject', edit_subject.as_view(), name = 'edit_subject'),
    path('delete_subject', delete_subject.as_view(), name = 'delete_subject'),
]