from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
student_list_url=frontend_url+'api/Parent_StudentMaster/getstudentlist'
search_student_by_class_and_year_url=frontend_url+'api/Parent_StudentMaster/search_student_by_class_and_year'
class_list_url=frontend_url+'api/ClassMaster/List'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
delete_student_url=frontend_url+'api/Parent_StudentMaster/deleteStudent'
update_student_url=frontend_url+'api/Parent_StudentMaster/update_student'
student_id_cards_url=frontend_url+'api/Parent_StudentMaster/getstudentidcards'
search_student_by_class_of_currentyear_url=frontend_url+'api/Parent_StudentMaster/search_student_by_class_of_currentyear'
bloodgroups_list_url = frontend_url+'api/Parent_StudentMaster/bloodgrouplist'

class student_list(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # student_list_request = requests.post(student_list_url,headers=headers)
            # student_list_response = student_list_request.json()
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
                        
            bloodgroups_list_request = requests.get(bloodgroups_list_url,headers=headers)
            bloodgroups_list_response = bloodgroups_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            
            return render(request, 'admin/student_master/studentlist.html',{'bloodgroups':bloodgroups_list_response['data'],
                                                                            'classes':class_list_response['data'],
                                                                            'academic_years':academic_list_response['data']})

        else:
            return redirect('school:login')


    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            student_list_request = requests.post(search_student_by_class_and_year_url,headers=headers,data=data)
            student_list_response = student_list_request.json()
            return HttpResponse(json.dumps(student_list_response), content_type="application/json")
        
class student_id_cards(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}

            student_list_request = requests.post(search_student_by_class_and_year_url,headers=headers)
            student_list_response = student_list_request.json()
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            return render(request, 'admin/student_master/studentcards.html',{'students':student_list_response['data'],
                                                                            'classes':class_list_response['data'],
                                                                            'academic_years':academic_list_response['data'],})

        else:
            return redirect('school:login')

    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            student_id_cards_request = requests.post(student_id_cards_url,headers=headers,data=data)
            student_id_cards_response = student_id_cards_request.json()
            return HttpResponse(json.dumps(student_id_cards_response), content_type="application/json")
        
class delete_student(GenericAPIView):

    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            delete_student_request = requests.post(delete_student_url, data=data,headers=headers)
            delete_student_response = delete_student_request.json()
            return HttpResponse(json.dumps(delete_student_response), content_type="application/json")

class update_student(GenericAPIView):

    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            update_student_request = requests.post(update_student_url, data=data,headers=headers)
            update_student_response = update_student_request.json()
            return HttpResponse(json.dumps(update_student_response), content_type="application/json")
        
class get_class_students(GenericAPIView):
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            get_class_students_request = requests.post(search_student_by_class_of_currentyear_url,headers=headers,data=data)
            get_class_students_response = get_class_students_request.json()
            return HttpResponse(json.dumps(get_class_students_response), content_type="application/json")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        