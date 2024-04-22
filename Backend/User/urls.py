from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', Adduser.as_view(), name = 'Add'),
]