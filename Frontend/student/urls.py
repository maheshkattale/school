from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('student_list', student_list.as_view(), name = 'student_list'),
    path('student_id_cards', student_id_cards.as_view(), name = 'student_id_cards'),

]