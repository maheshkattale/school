from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
  
    path('Add', AddSchool.as_view(), name = 'Add'),
]