from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', addtimetable.as_view(), name = 'Add'),
    path('getteachersfromsub', getteachersfromsub.as_view(), name = 'getteachersfromsub'),
   

]