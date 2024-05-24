from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
forget_password_url=frontend_url+'api/User/forgetpasswordmail'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
class_list_url=frontend_url+'api/ClassMaster/List'
add_fees_distributions_for_multiple_class_url=frontend_url+'api/FeesMaster/add_fees_distributions_for_multiple_class'
fees_destributiom_list_url=frontend_url+'api/FeesMaster/fees_destributiom_list'
delete_fees_distributions_url=frontend_url+'api/FeesMaster/delete_fees_distributions'
fees_distribution_details_url=frontend_url+'api/FeesMaster/get_fees_distributions_details'
edit_fees_distributions_for_multiple_class_url=frontend_url+'api/FeesMaster/edit_fees_distributions_for_multiple_class'
# Create your views here.

class fees_distrubution(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            fees_destributiom_list_request = requests.get(fees_destributiom_list_url,headers=headers)
            fees_destributiom_list_response = fees_destributiom_list_request.json()
            return render(request, 'admin/fees_master/fees_distribution.html',{'fees':fees_destributiom_list_response['data']})
        else:
            return redirect('school:login')
class add_fees_distrubution(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            return render(request, 'admin/fees_master/add_fees_distribution.html',{'academic_years':academic_list_response['data'],'classes':class_list_response['data'],})
        else:
            return redirect('school:login')
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_fees_distrubution_request = requests.post(add_fees_distributions_for_multiple_class_url,headers=headers,data=data)
            add_fees_distrubution_response = add_fees_distrubution_request.json()
            return HttpResponse(json.dumps(add_fees_distrubution_response), content_type="application/json")
class delete_fees(GenericAPIView):

        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_fees_distrubution_request = requests.post(delete_fees_distributions_url,headers=headers,data=data)
            delete_fees_distrubution_response = delete_fees_distrubution_request.json()
            return HttpResponse(json.dumps(delete_fees_distrubution_response), content_type="application/json")
        
        
        
        
class edit_fees_distribution(GenericAPIView):
    def get(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['id']=id
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            fees_distribution_details_request = requests.post(fees_distribution_details_url,headers=headers,data=data)
            fees_distribution_details_response = fees_distribution_details_request.json()
            print("fees_distribution_details_response",fees_distribution_details_response)
            return render(request, 'admin/fees_master/edit_fees_distribution.html',{'academic_years':academic_list_response['data'],'classes':class_list_response['data'],'fee':fees_distribution_details_response['data']})
        else:
            return redirect('school:login')
        
    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['id']=id
            edit_fees_distrubution_request = requests.post(edit_fees_distributions_for_multiple_class_url,headers=headers,data=data)
            edit_fees_distrubution_response = edit_fees_distrubution_request.json()
            return HttpResponse(json.dumps(edit_fees_distrubution_response), content_type="application/json")
        
        
        
        
        
        