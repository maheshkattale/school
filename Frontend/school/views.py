from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .static_info import frontend_url
# Create your views here.
login_url=frontend_url+"api/User/login"
logout_url = frontend_url+'api/User/logout'
school_list_url=frontend_url+'api/SchoolMaster/list'
add_school_url=frontend_url+'api/SchoolMaster/Add'
disable_school_url=frontend_url+'api/SchoolMaster/disable'
enable_school_url=frontend_url+'api/SchoolMaster/enable'
get_school_info_url=frontend_url+'api/SchoolMaster/getbyid'
edit_school_url=frontend_url+'api/SchoolMaster/update'

# student_list_url=frontend_url+'api/Parent_StudentMaster/getstudentlist'
class_list_url=frontend_url+'api/ClassMaster/List'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'


class login(GenericAPIView):
    def get(self,request):
        return render(request, 'login.html',{})
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        source = request.POST['source']
        data = {}
        data['email'] = email
        data['password'] = password
        data['source'] = source
        
        
        login_request = requests.post(login_url, data=data)
        login_response = login_request.json()
        if login_response['response']['n']==0:
            msg = login_response['response']['msg']
            messages.error(request, msg)
            return redirect('school:login')
        
        else:
            request.session['token'] = login_response['data']['token']
            request.session['schoolcode'] = login_response['data']['schoolcode']
            request.session['username'] = login_response['data']['username']
            request.session['user_id'] = login_response['data']['user_id']
            request.session['Menu'] = login_response['data']['Menu']
            request.session['email'] = login_response['data']['email']
            request.session['mobileNumber'] = login_response['data']['mobileNumber']
            request.session['Address'] = login_response['data']['Address']
            request.session['roleid'] = login_response['data']['roleid']
            request.session['children_list'] = login_response['data']['children_list']
            request.session['PrimaryStudentId'] = login_response['data']['PrimaryStudentId']
            request.session['PrimaryStudentCode'] = login_response['data']['PrimaryStudentCode']

            # msg = login_response['response']['msg']
            # messages.success(request, msg)
            return redirect('school:dashboard')


class logout(GenericAPIView):
    def get(self,request):
        try:
            tok = request.session.get('token', False)
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            logout_request = requests.post(logout_url, headers=headers)
            logout_response = logout_request.json()
            if logout_response['response']['n'] == 1:
                del request.session['token']
                messages.success(request, logout_response['response']['msg'])
                return redirect('school:login')
            else:
                messages.error(request, logout_response['response']['msg'])
                return redirect('school:login')
        except Exception as e:
            messages.error(request, e)
            return redirect('school:login')




class dashboard(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            return render(request, 'admin/dashboard.html',{})

        messages.error(request, 'Session expired please login again')
        return redirect('school:login')
    

    
    
class school_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            school_list_request = requests.get(school_list_url, headers=headers)
            school_list_response = school_list_request.json()
            return render(request, 'superadmin/school_master.html',{'schools':school_list_response['data']})
        else:
            return redirect('school:login')
            
    
class add_school(GenericAPIView):
    def get(self,request):
        return render(request, 'superadmin/add_school.html',{})
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            files={}
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            files['school_logo'] = request.FILES.get('school_logo')

            add_school_request = requests.post(add_school_url, data=data,files=files, headers=headers)
            add_school_response = add_school_request.json()
            return HttpResponse(json.dumps(add_school_response), content_type="application/json")

        
class disable_school(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            disable_school_request = requests.post(disable_school_url, data=data,headers=headers)
            disable_school_response = disable_school_request.json()
            return HttpResponse(json.dumps(disable_school_response), content_type="application/json")
        
        
class enable_school(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            enable_school_request = requests.post(enable_school_url, data=data,headers=headers)
            enable_school_response = enable_school_request.json()
            return HttpResponse(json.dumps(enable_school_response), content_type="application/json")
        

class edit_school(GenericAPIView):
    def get(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            data['id']=id
            get_school_info_request = requests.post(get_school_info_url,headers=headers,data=data)
            get_school_info_response = get_school_info_request.json()
            return render(request, 'superadmin/edit_school.html',{'school':get_school_info_response['data']})
        
    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            files={}
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            files['school_logo'] = request.FILES.get('school_logo')
            edit_school_request = requests.post(edit_school_url, data=data,files=files,headers=headers)
            edit_school_response = edit_school_request.json()
            return HttpResponse(json.dumps(edit_school_response), content_type="application/json")

        
class mail(GenericAPIView):
    def get(self,request):
        return render(request, 'mails/teacher_registration.html',{"Name": 'mahesh kattale',"email":'maheshkattale@gmail.com','userid':'887ddc8c-ef0d-49f3-bc80-3afa47f52fd8','frontend_url':frontend_url,'school_name':'Shri Vidya Bhavan School',"adminname": 'mahesh kattale','adminid':'887ddc8c-ef0d-49f3-bc80-3afa47f52fd8', 'bestregard_from':'School ERP','phone_no':'0201-890890',})


class template_render(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/student_master/student_id_cards_pdf.html',{"Name": 'mahesh kattale',"email":'maheshkattale@gmail.com','userid':'887ddc8c-ef0d-49f3-bc80-3afa47f52fd8','frontend_url':frontend_url,'school_name':'Shri Vidya Bhavan School',"adminname": 'mahesh kattale','adminid':'887ddc8c-ef0d-49f3-bc80-3afa47f52fd8', 'bestregard_from':'School ERP','phone_no':'0201-890890',})
    

class reset_password_mail(GenericAPIView):
    def get(self,request):
        return render(request, 'mails/reset_password.html',{'Admin_Name':'Mahesh Kattale','frontend_url':frontend_url})


class marksheet(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            return render(request, 'admin/marksheet_master/marksheet.html',{'classes':class_list_response['data'],'academic_years':academic_list_response['data'],})
        else:
            return redirect('school:login')
    

class permissions(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/permissions.html',{})
    
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)