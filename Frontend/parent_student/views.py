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
set_primary_student_url = frontend_url+'api/Parent_StudentMaster/set_primary_student'
announcements_list_url= frontend_url+'api/Parent_StudentMaster/announcement_list'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
add_announcements_url=frontend_url+'api/Parent_StudentMaster/add_announcement'
delete_announcements_url=frontend_url+'api/Parent_StudentMaster/delete_announcement'
get_announcement_details_url=frontend_url+'api/Parent_StudentMaster/get_announcement_details'
edit_announcements_url=frontend_url+'api/Parent_StudentMaster/edit_announcement'
search_students_url=frontend_url+'api/Parent_StudentMaster/search_students'

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
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            student_delete_request = requests.post(student_delete_url,headers=headers,data=data)
            student_delete_response = student_delete_request.json()
            return HttpResponse(json.dumps(student_delete_response), content_type="application/json")
        
        
class set_primary_student(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            set_primary_student_request = requests.post(set_primary_student_url,headers=headers,data=data)
            set_primary_student_response = set_primary_student_request.json()
            if set_primary_student_response['response']['n']==1:
                request.session['PrimaryStudentId'] = set_primary_student_response['data']['id']
                request.session['PrimaryStudentCode'] = set_primary_student_response['data']['StudentCode']
                
            return HttpResponse(json.dumps(set_primary_student_response), content_type="application/json")
        
        
class announcements(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            announcements_list_request = requests.get(announcements_list_url,headers=headers)
            announcements_list_response = announcements_list_request.json()
            
            
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            return render(request, 'admin/announcement_master/announcements.html',{'classes':class_list_response['data'],'academic_years':academic_list_response['data'],'announcementslist':announcements_list_response['data']})
        else:
            return redirect('school:login')
        

class add_announcements(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_announcements_request = requests.post(add_announcements_url,headers=headers,data=data)
            add_announcements_response = add_announcements_request.json()
            return HttpResponse(json.dumps(add_announcements_response), content_type="application/json")
class delete_announcements(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_announcements_request = requests.post(delete_announcements_url,headers=headers,data=data)
            delete_announcements_response = delete_announcements_request.json()
            return HttpResponse(json.dumps(delete_announcements_response), content_type="application/json")
class edit_announcements(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            edit_announcements_request = requests.post(edit_announcements_url,headers=headers,data=data)
            edit_announcements_response = edit_announcements_request.json()
            return HttpResponse(json.dumps(edit_announcements_response), content_type="application/json")
class get_announcement_details(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            get_announcement_details_request = requests.post(get_announcement_details_url,headers=headers,data=data)
            get_announcement_details_response = get_announcement_details_request.json()
            return HttpResponse(json.dumps(get_announcement_details_response), content_type="application/json")
        
        
        
        
        
class search_students(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            search_students_request = requests.post(search_students_url,headers=headers,data=data)
            search_students_response = search_students_request.json()

            return HttpResponse(json.dumps(search_students_response), content_type="application/json")
        
        
        
        
        