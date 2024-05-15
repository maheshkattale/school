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