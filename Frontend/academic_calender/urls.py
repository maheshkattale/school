from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', academic_calender.as_view(), name = 'academic_calender'),
    path('get_academic_calender_events', get_academic_calender_events.as_view(), name = 'get_academic_calender_events'),
 
    
    
]