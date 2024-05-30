from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    #examtypemaster
    path('Add', AddExamType.as_view(), name = 'Add'),
    path('List', ExamTypelist.as_view(), name = 'list'),
    path('getbyid',ExamTypebyid.as_view(), name = 'getbyid'),
    path('update', updateExamType.as_view(), name = 'update'),
    path('delete', deleteExamType.as_view(), name = 'delete'),
    
    path('examscorelist', examscorelist.as_view(), name = 'examscorelist'),
    path('add_exam_type_marks', AddExamTypeMarks.as_view(), name = 'add_exam_type_marks'),
    path('exam_type_marks_list', exam_type_marks_list.as_view(), name = 'exam_type_marks_list'),
    path('delete_exam_type_marks', delete_exam_type_marks.as_view(), name = 'delete_exam_type_marks'),
    path('edit_exam_type_marks', edit_exam_type_marks.as_view(), name = 'edit_exam_type_marks'),
    path('get_marks_by_exam_type', get_marks_by_exam_type.as_view(), name = 'get_marks_by_exam_type'),


    #exammaster
    path('AddExam', AddExam.as_view(), name = 'AddExam'),
    path('Examlist', Examlist.as_view(), name = 'Examlist'),
    path('Exambyid', Exambyid.as_view(), name = 'Exambyid'),
    path('updateexam', updateexam.as_view(), name = 'updateexam'),
    path('deleteexam', deleteexam.as_view(), name = 'deleteexam'),

    path('uploadmarksheet', uploadmarksheet.as_view(), name = 'uploadmarksheet'),
    
    
    #marksheet
    path('UploadExcelMarkSheet', UploadExcelMarkSheet.as_view(), name = 'UploadExcelMarkSheet'),

    # exam name
    path('exam_names_list', exam_names_list.as_view(), name = 'exam_names_list'),
    path('exam_by_academicyear_list', exam_by_academicyear_list.as_view(), name = 'exam_by_academicyear_list'),

]