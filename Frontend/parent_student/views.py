from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'
parent_list_url = frontend_url+'api/Parent_StudentMaster/list'
getparentinfourl = frontend_url+'api/Parent_StudentMaster/getbyid'
bloodgrouplisturl = frontend_url+'api/Parent_StudentMaster/bloodgrouplist'
parent_delete_url = frontend_url+'api/Parent_StudentMaster/delete'
student_delete_url = frontend_url+'api/Parent_StudentMaster/deleteStudent'

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
            get_blood_info_request = requests.get(bloodgrouplisturl,headers=headers)
            bloodgresp = get_blood_info_request.json()
            return render(request, 'admin/parent_student_master/add_parent_student.html',{'classlist':class_list_response['data'],'bloodgrplist':bloodgresp['data']})
        else:
            return redirect('school:login')
    
class edit_parent_student(GenericAPIView):
      def get(self,request,id):

        tok = request.session.get('token', False)
        if tok:
            print("byy")
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            data={}
            data['id']=id
            get_parent_info_request = requests.post(getparentinfourl,headers=headers,data=data)
            parentresp = get_parent_info_request.json()
            get_blood_info_request = requests.get(bloodgrouplisturl,headers=headers)
            bloodgresp = get_blood_info_request.json()
            
            return render(request, 'admin/parent_student_master/edit_parent_student.html',{'classlist':class_list_response['data'],'parentsinfo':parentresp['data'],'bloodgrplist':bloodgresp['data']})

   
class student_list(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/student_cards.html',{})
    

class delete_parent(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            parent_delete_request = requests.post(parent_delete_url,headers=headers,data=data)
            parent_delete_response = parent_delete_request.json()
            return HttpResponse(json.dumps(parent_delete_response), content_type="application/json")
        

class delete_student(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            print("front")
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            student_delete_request = requests.post(student_delete_url,headers=headers,data=data)
            student_delete_response = student_delete_request.json()
            return HttpResponse(json.dumps(student_delete_response), content_type="application/json")