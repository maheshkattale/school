from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('generate_marksheet', generate_marksheet.as_view(), name = 'generate_marksheet'),

    
]