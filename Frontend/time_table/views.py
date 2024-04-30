from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
subject_list_url=frontend_url+'api/SubjectMaster/List'
teacher_list_url=frontend_url+'api/TeacherMaster/list'
class_list_url=frontend_url+'api/ClassMaster/List'

class time_table_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/time_table_master.html',{})
    
class add_time_table(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}

            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            teacher_list_request = requests.get(teacher_list_url,headers=headers)
            teacher_list_response = teacher_list_request.json()
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            context={
                'subjects':subject_list_response['data'],
                'teachers':teacher_list_response['data'],
                'classes':class_list_response['data'],
            }
            return render(request, 'admin/time_table_master/add_time_table.html',context)
        else:
            return redirect('school:login')

class edit_time_table(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/edit_time_table.html',{})