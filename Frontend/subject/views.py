from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
subject_list_url=frontend_url+'api/SubjectMaster/List'
subject_add_url=frontend_url+'api/SubjectMaster/Add'
subject_edit_url=frontend_url+'api/SubjectMaster/update'
subject_delete_url=frontend_url+'api/SubjectMaster/delete'

class subject_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            print("subject_list_response",subject_list_response)
            if subject_list_response['response']['n']==1:
                return render(request, 'admin/subject_master/subject_master.html',{'subjects':subject_list_response['data']})
            else:
                messages.error(request, subject_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, subject_list_response['response']['msg'])
            return redirect('school:login')
        
class add_subject(GenericAPIView):
    def post(self,request):
        

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            subject_add_request = requests.post(subject_add_url,headers=headers,data=data)
            subject_add_response = subject_add_request.json()
            print("subject_add_response",subject_add_response)
            return HttpResponse(json.dumps(subject_add_response), content_type="application/json")

           
    
class edit_subject(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            subject_edit_request = requests.post(subject_edit_url,headers=headers,data=data)
            subject_edit_response = subject_edit_request.json()
            print("subject_edit_response",subject_edit_response)
            return HttpResponse(json.dumps(subject_edit_response), content_type="application/json")
        
class delete_subject(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            subject_delete_request = requests.post(subject_delete_url,headers=headers,data=data)
            subject_delete_response = subject_delete_request.json()
            print("subject_delete_response",subject_delete_response)
            return HttpResponse(json.dumps(subject_delete_response), content_type="application/json")