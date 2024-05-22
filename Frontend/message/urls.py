from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', messages.as_view(), name = 'messages'),
    path('add_message', add_message.as_view(), name = 'add_message'),

    
]