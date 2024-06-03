from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'
class_add_url=frontend_url+'api/ClassMaster/Add'
class_edit_url=frontend_url+'api/ClassMaster/update'
class_delete_url=frontend_url+'api/ClassMaster/delete'
teachers_list_url=frontend_url+'api/TeacherMaster/list'
academic_years_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
add_class_teacher_url=frontend_url+'api/ClassMaster/add_class_teacher'
edit_class_teacher_url=frontend_url+'api/ClassMaster/edit_class_teacher'
get_class_teachers_url=frontend_url+'api/ClassMaster/get_class_teachers'
delete_class_teacher_url=frontend_url+'api/ClassMaster/delete_class_teacher'
class class_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            if class_list_response['response']['n']==1:
                return render(request, 'admin/class_master/class_master.html',{'classes':class_list_response['data']})
            else:
                messages.error(request, class_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, class_list_response['response']['msg'])
            return redirect('school:login')
              
class add_class(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            class_add_request = requests.post(class_add_url,headers=headers,data=data)
            class_add_response = class_add_request.json()
            return HttpResponse(json.dumps(class_add_response), content_type="application/json")

           
    
class edit_class(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            class_edit_request = requests.post(class_edit_url,headers=headers,data=data)
            class_edit_response = class_edit_request.json()
            return HttpResponse(json.dumps(class_edit_response), content_type="application/json")
        
class delete_class(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            class_delete_request = requests.post(class_delete_url,headers=headers,data=data)
            class_delete_response = class_delete_request.json()
            return HttpResponse(json.dumps(class_delete_response), content_type="application/json")
        
class class_teachers(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()

            teachers_list_request = requests.get(teachers_list_url,headers=headers)
            teachers_list_response = teachers_list_request.json()

            academic_years_list_request = requests.get(academic_years_list_url,headers=headers)
            academic_years_list_response = academic_years_list_request.json()

            get_class_teachers_request = requests.get(get_class_teachers_url,headers=headers)
            get_class_teachers_response = get_class_teachers_request.json()
            
            if class_list_response['response']['n']==1:
                return render(request, 'admin/teacher_master/class_teachers_master.html',{'classes':class_list_response['data'],'teachers':teachers_list_response['data'],'academic_years':academic_years_list_response['data'],'class_teachers':get_class_teachers_response['data']})
            else:
                messages.error(request, class_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, class_list_response['response']['msg'])
            return redirect('school:login')

class add_class_teacher(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_class_teacher_request = requests.post(add_class_teacher_url,headers=headers,data=data)
            add_class_teacher_response = add_class_teacher_request.json()
            return HttpResponse(json.dumps(add_class_teacher_response), content_type="application/json")

class delete_class_teacher(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_class_teacher_request = requests.post(delete_class_teacher_url,headers=headers,data=data)
            delete_class_teacher_response = delete_class_teacher_request.json()
            return HttpResponse(json.dumps(delete_class_teacher_response), content_type="application/json")
        
class edit_class_teacher(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            edit_class_teacher_request = requests.post(edit_class_teacher_url,headers=headers,data=data)
            edit_class_teacher_response = edit_class_teacher_request.json()
            return HttpResponse(json.dumps(edit_class_teacher_response), content_type="application/json")

# pbkdf2_sha256$390000$3tApMBhCjIaBr7kICFQECI$gmCAvWwS/lMTo2gusEKC2J1tRRFIqkkw4sYiiJOtdKg=



































