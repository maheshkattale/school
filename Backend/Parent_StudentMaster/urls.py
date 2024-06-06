from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Add', AddParentStudent.as_view(), name = 'Add'),
    path('list', ParentStudentlist.as_view(), name = 'list'),
    path('getbyid', getParentStudentbyid.as_view(), name = 'getbyid'),
    path('update', updateParentStudent.as_view(), name = 'update'),
    path('delete', deleteParent.as_view(), name = 'delete'),

    path('studentlist', studentlist.as_view(), name = 'studentlist'),
    path('studentsbyclasslist', studentsbyclasslist.as_view(), name = 'studentsbyclasslist'),
    path('studentsbyparentlist', studentsbyparentlist.as_view(), name = 'studentsbyparentlist'),
    path('bloodgrouplist', bloodgrouplist.as_view(), name = 'bloodgrouplist'),
    path('deleteStudent', deleteStudent.as_view(), name = 'deleteStudent'),
    
    path('search_student_by_class_and_year', search_student_by_class_and_year.as_view(), name = 'search_student_by_class_and_year'),
    path('getstudentlist', getstudentlist.as_view(), name = 'getstudentlist'),
    path('getstudentidcards', getstudentidcards.as_view(), name = 'getstudentidcards'),
    path('set_primary_student', set_primary_student.as_view(), name = 'set_primary_student'),
    path('search_student_by_class_of_currentyear', search_student_by_class_of_currentyear.as_view(), name = 'search_student_by_class_of_currentyear'),

    #announcements
    path('add_announcement', add_announcement.as_view(), name = 'add_announcement'),
    path('edit_announcement', edit_announcement.as_view(), name = 'edit_announcement'),
    path('announcement_list', announcement_list.as_view(), name = 'announcement_list'),
    path('get_announcement_details', get_announcement_details.as_view(), name = 'get_announcement_details'),
    path('delete_announcement', delete_announcement.as_view(), name = 'delete_announcement'),
    path('get_student_announcements', get_student_announcements.as_view(), name = 'get_student_announcements'),
    
    # 
    path('getPromotedList', getPromotedList.as_view(), name = 'getPromotedList'),
    
    
]