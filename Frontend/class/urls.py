from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', class_master.as_view(), name = 'class_master'),
    path('add_class', add_class.as_view(), name = 'add_class'),
    path('edit_class', edit_class.as_view(), name = 'edit_class'),
    
    
]