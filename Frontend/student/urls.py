from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('student_list', student_list.as_view(), name = 'student_list'),
    path('student_id_cards', student_id_cards.as_view(), name = 'student_id_cards'),
    path('delete_student', delete_student.as_view(), name = 'delete_student'),
    path('update_student', update_student.as_view(), name = 'update_student'),
    path('get_class_students', get_class_students.as_view(), name = 'get_class_students'),

]