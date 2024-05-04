from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'


class exam(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # exam_request = requests.get(exam_url,headers=headers)
            # exam_response = exam_request.json()
            return render(request, 'admin/exam/exam_master.html',{})
        else:
            return redirect('school:login')
        
class edit_exam(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # exam_request = requests.get(exam_url,headers=headers)
            # exam_response = exam_request.json()
            return render(request, 'admin/exam/edit_exam.html',{})
        else:
            return redirect('school:login')
        
class add_exam(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # exam_request = requests.get(exam_url,headers=headers)
            # exam_response = exam_request.json()
            return render(request, 'admin/exam/add_exam.html',{})
        else:
            return redirect('school:login')
        
        
        
        
        
        
class exam_type(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}

            return render(request, 'admin/exam_type/exam_type_master.html',{})
        else:
            return redirect('school:login')
        
        
        
        
        