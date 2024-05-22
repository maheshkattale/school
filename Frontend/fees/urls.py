from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('fees_distrubution', fees_distrubution.as_view(), name = 'fees_distrubution'),
]