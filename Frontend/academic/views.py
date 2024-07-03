from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
add_academic_dates_url=frontend_url+'api/SchoolMaster/AddAcademicYear'
edit_academic_dates_url=frontend_url+'api/SchoolMaster/updateAcademicYear'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
delete_academic_dates_url=frontend_url+'api/SchoolMaster/deleteAcademicYear'
toggleAcademicYear_url=frontend_url+'api/SchoolMaster/toggleAcademicYear'
enableAcademicYear_url=frontend_url+'api/SchoolMaster/enableAcademicYear'


class academic_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            print('academic_list_response',academic_list_response['data'])
            return render(request, 'admin/academic/academic_master.html',{'academics':academic_list_response['data']})
    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_academic_dates_request = requests.post(add_academic_dates_url,data=data,headers=headers)
            add_academic_dates_response = add_academic_dates_request.json()
            return HttpResponse(json.dumps(add_academic_dates_response), content_type="application/json")
        else:
            return redirect('school:login')
        
        
        
class edit_academic(GenericAPIView):

    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            edit_academic_dates_request = requests.post(edit_academic_dates_url,data=data,headers=headers)
            edit_academic_dates_response = edit_academic_dates_request.json()
            return HttpResponse(json.dumps(edit_academic_dates_response), content_type="application/json")
        else:
            return redirect('school:login')

class delete_academic(GenericAPIView):

    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_academic_dates_request = requests.post(delete_academic_dates_url,data=data,headers=headers)
            delete_academic_dates_response = delete_academic_dates_request.json()
            return HttpResponse(json.dumps(delete_academic_dates_response), content_type="application/json")
        else:
            return redirect('school:login')
        
class toggleAcademicYear(GenericAPIView):

    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            
            toggleAcademicYear_request = requests.post(toggleAcademicYear_url,headers=headers,data=data)
            toggleAcademicYear_response = toggleAcademicYear_request.json()
            return HttpResponse(json.dumps(toggleAcademicYear_response), content_type="application/json")
        else:
            return redirect('school:login')
        
class enableAcademicYear(GenericAPIView):

    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            
            enableAcademicYear_request = requests.post(enableAcademicYear_url,headers=headers,data=data)
            enableAcademicYear_response = enableAcademicYear_request.json()
            return HttpResponse(json.dumps(enableAcademicYear_response), content_type="application/json")
        else:
            return redirect('school:login')
        
        
        
        
        
        
        
        