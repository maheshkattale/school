from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', designation_master.as_view(), name = 'designation_master'),
    path('add_designation', add_designation.as_view(), name = 'add_designation'),
    path('edit_designation', edit_designation.as_view(), name = 'edit_designation'),
    path('delete_designation', delete_designation.as_view(), name = 'delete_designation'),
    
]