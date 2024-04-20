from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', time_table_master.as_view(), name = 'time_table_master'),
    path('add_time_table', add_time_table.as_view(), name = 'add_time_table'),
    path('edit_time_table', edit_time_table.as_view(), name = 'edit_time_table'),
    
    
]