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
student_pending_fees_url=frontend_url+'api/FeesMaster/get_student_pending_fees_list'
student_list_url=frontend_url+'api/Parent_StudentMaster/getstudentlist'
pay_student_fees_url=frontend_url+'api/FeesMaster/pay_student_fees'
edit_fees_distributions_for_multiple_class_url=frontend_url+'api/FeesMaster/edit_fees_distributions_for_multiple_class'
student_pending_fees_by_id_url=frontend_url+'api/FeesMaster/get_student_pending_fees_list_by_id'
search_student_by_class_and_year_url=frontend_url+'api/Parent_StudentMaster/search_student_by_class_and_year'

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
        
class student_fees(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['StudentCode']=request.session.get('PrimaryStudentCode')
            student_pending_fees_request = requests.post(student_pending_fees_url,data=data,headers=headers)
            student_pending_fees_response = student_pending_fees_request.json()
            return render(request, 'admin/fees_master/student_fees.html',{'fees':student_pending_fees_response['data'],})
        else:
            return redirect('school:login')
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['StudentCode']=request.session.get('PrimaryStudentCode')
            pay_student_fees_request = requests.post(pay_student_fees_url,headers=headers,data=data)
            pay_student_fees_response = pay_student_fees_request.json()
            return HttpResponse(json.dumps(pay_student_fees_response), content_type="application/json")
        
class students_fees(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            # student_list_request = requests.post(search_student_by_class_and_year_url,headers=headers)
            # student_list_response = student_list_request.json()
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            
            return render(request, 'admin/fees_master/students_list.html',{
                                                                            'classes':class_list_response['data'],
                                                                            'academic_years':academic_list_response['data'],})
        
        
        else:
            return redirect('school:login')
        
class student_fee(GenericAPIView):
    def get(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['id']=id
            student_pending_fees_request = requests.post(student_pending_fees_by_id_url,data=data,headers=headers)
            student_pending_fees_response = student_pending_fees_request.json()
            return render(request, 'admin/fees_master/student_fees_history.html',{'fees':student_pending_fees_response['data'],'student':student_pending_fees_response['student']})
        else:
            return redirect('school:login')
        

class pay_student_fee(GenericAPIView):

    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['StudentCode']=request.POST.get('StudentCode')
            pay_student_fees_request = requests.post(pay_student_fees_url,headers=headers,data=data)
            pay_student_fees_response = pay_student_fees_request.json()
            return HttpResponse(json.dumps(pay_student_fees_response), content_type="application/json")
   


        
        
        
        
        
        
        