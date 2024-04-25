from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
teacher_list_url=frontend_url+'api/TeacherMaster/list'
teacher_add_url=frontend_url+'api/TeacherMaster/Add'
teacher_edit_url=frontend_url+'api/TeacherMaster/update'
teacher_delete_url=frontend_url+'api/TeacherMaster/delete'
designation_list_url=frontend_url+'api/DesignationMaster/List'
get_teacher_info_url=frontend_url+'api/TeacherMaster/getbyid'
subject_list_url=frontend_url+'api/SubjectMaster/List'
class teacher_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            teacher_list_request = requests.get(teacher_list_url,headers=headers)
            teacher_list_response = teacher_list_request.json()
            if teacher_list_response['response']['n']==1:
                return render(request, 'admin/teacher_master/teacher_master.html',{'teachers':teacher_list_response['data']})
            else:
                messages.error(request, teacher_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, teacher_list_response['response']['msg'])
            return redirect('school:login')
        
class add_teacher(GenericAPIView):
    def get(self,request):
        
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            designation_list_request = requests.get(designation_list_url,headers=headers)
            designation_list_response = designation_list_request.json()
            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            return render(request, 'admin/teacher_master/add_teacher.html',{'designations':designation_list_response['data'],'subjects':subject_list_response['data']})
    

    def post(self,request):
        
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            
            teacher_add_request = requests.post(teacher_add_url,headers=headers,data=data)
            teacher_add_response = teacher_add_request.json()
            return HttpResponse(json.dumps(teacher_add_response), content_type="application/json")

           
    
class edit_teacher(GenericAPIView):
    def get(self,request,id):

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            designation_list_request = requests.get(designation_list_url,headers=headers)
            designation_list_response = designation_list_request.json()
            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            data={}
            data['id']=id
            get_teacher_info_request = requests.post(get_teacher_info_url,headers=headers,data=data)
            get_teacher_info_response = get_teacher_info_request.json()
            
            return render(request, 'admin/teacher_master/edit_teacher.html',{'designations':designation_list_response['data'],'subjects':subject_list_response['data'],'teacher':get_teacher_info_response['data'],'teacher_subjects':get_teacher_info_response['subjectidlist']})
    

    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:

            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            
            teacher_edit_request = requests.post(teacher_edit_url,headers=headers,data=data)
            teacher_edit_response = teacher_edit_request.json()
            return HttpResponse(json.dumps(teacher_edit_response), content_type="application/json")

           
        
class delete_teacher(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            teacher_delete_request = requests.post(teacher_delete_url,headers=headers,data=data)
            teacher_delete_response = teacher_delete_request.json()
            return HttpResponse(json.dumps(teacher_delete_response), content_type="application/json")