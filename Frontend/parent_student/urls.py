from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', parent_student_master.as_view(), name = 'parent_student_master'),
    path('add_parent_student', add_parent_student.as_view(), name = 'add_parent_student'),
    path('edit_parent_student/<str:id>', edit_parent_student.as_view(), name = 'edit_parent_student'),
    path('student_list', student_list.as_view(), name = 'student_list'),
    path('delete_parent', delete_parent.as_view(), name = 'delete_parent'),
    path('delete_student', delete_student.as_view(), name = 'delete_student'),
    path('set_primary_student', set_primary_student.as_view(), name = 'set_primary_student'),
    path('search_students', search_students.as_view(), name = 'search_students'),
    path('promote_students_class', promote_students_class.as_view(), name = 'promote_students_class'),
    
    
    # announcements
    path('announcements', announcements.as_view(), name = 'announcements'),
    path('add_announcements', add_announcements.as_view(), name = 'add_announcements'),
    path('delete_announcements', delete_announcements.as_view(), name = 'delete_announcements'),
    path('get_announcement_details', get_announcement_details.as_view(), name = 'get_announcement_details'),
    path('edit_announcements', edit_announcements.as_view(), name = 'edit_announcements'),

]