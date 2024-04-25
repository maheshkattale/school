from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
designation_list_url=frontend_url+'api/DesignationMaster/List'
designation_add_url=frontend_url+'api/DesignationMaster/Add'
designation_edit_url=frontend_url+'api/DesignationMaster/update'
designation_delete_url=frontend_url+'api/DesignationMaster/delete'

class designation_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            designation_list_request = requests.get(designation_list_url,headers=headers)
            designation_list_response = designation_list_request.json()
            if designation_list_response['response']['n']==1:
                return render(request, 'admin/designation_master/designation_master.html',{'designations':designation_list_response['data']})
            else:
                messages.error(request, designation_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, designation_list_response['response']['msg'])
            return redirect('school:login')
        
class add_designation(GenericAPIView):
    def post(self,request):
        

        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            designation_add_request = requests.post(designation_add_url,headers=headers,data=data)
            designation_add_response = designation_add_request.json()
            return HttpResponse(json.dumps(designation_add_response), content_type="application/json")

           
    
class edit_designation(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            designation_edit_request = requests.post(designation_edit_url,headers=headers,data=data)
            designation_edit_response = designation_edit_request.json()
            return HttpResponse(json.dumps(designation_edit_response), content_type="application/json")
        
class delete_designation(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            designation_delete_request = requests.post(designation_delete_url,headers=headers,data=data)
            designation_delete_response = designation_delete_request.json()
            return HttpResponse(json.dumps(designation_delete_response), content_type="application/json")