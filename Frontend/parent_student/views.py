from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'
parent_list_url = frontend_url+'api/Parent_StudentMaster/list'


class parent_student_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            parent_list_request = requests.get(parent_list_url,headers=headers)
            parent_list_response = parent_list_request.json()
            return render(request, 'admin/parent_student_master/parent_student_master.html',{'parentlist':parent_list_response['data']})
        else:
            return redirect('school:login')

      
    
class add_parent_student(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            return render(request, 'admin/parent_student_master/add_parent_student.html',{'classlist':class_list_response['data']})
        else:
            return redirect('school:login')
    
class edit_parent_student(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/edit_parent_student.html',{})
class student_list(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/student_cards.html',{})