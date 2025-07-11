from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .static_info import frontend_url,image_url
# Create your views here.
login_url=frontend_url+"api/User/login"
logout_url = frontend_url+'api/User/logout'
school_list_url=frontend_url+'api/SchoolMaster/list'
add_school_url=frontend_url+'api/SchoolMaster/Add'
disable_school_url=frontend_url+'api/SchoolMaster/disable'
enable_school_url=frontend_url+'api/SchoolMaster/enable'
get_school_info_url=frontend_url+'api/SchoolMaster/getbyid'
edit_school_url=frontend_url+'api/SchoolMaster/update'
get_announcements_url=frontend_url+'api/Parent_StudentMaster/get_student_announcements'
get_admin_dashboard_details_url=frontend_url+'api/User/get_admin_dashboard_details'
get_teacher_dashboard_details_url=frontend_url+'api/User/get_teacher_dashboard_details'
# student_list_url=frontend_url+'api/Parent_StudentMaster/getstudentlist'
class_list_url=frontend_url+'api/ClassMaster/List'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'

exam_names_list_url=frontend_url+'api/MarksheetMaster/exam_names_list'
UploadExcelMarkSheet_url=frontend_url+'api/MarksheetMaster/UploadExcelMarkSheet'
student_list_url=frontend_url+'api/Parent_StudentMaster/getstudentlist'
search_students_url=frontend_url+'api/Parent_StudentMaster/search_students'
GenerateMarkSheet_url=frontend_url+'api/MarksheetMaster/GenerateMarkSheet'
sub_url=frontend_url+'api/SubjectMaster/List'
search_user_url=frontend_url+'api/User/search_user'
search_student_url=frontend_url+'api/Parent_StudentMaster/search_student'

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
            request.session['school_logo'] = login_response['data']['school_logo']
            request.session['user_role_name'] = login_response['data']['user_role_name']
            if login_response['data']['user_info']['photo'] is not None and login_response['data']['user_info']['photo'] !='':
                request.session['profile_image'] = image_url+login_response['data']['user_info']['photo']
            else:
                request.session['profile_image'] = ''
                
            if login_response['data']['school_info'] !=[]:
                request.session['school_name'] = login_response['data']['school_info']['Name']

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
            print("e",e)
            messages.error(request, e)
            return redirect('school:login')




class dashboard(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            if request.session.get('roleid') == 1:
                return redirect("school:school_master")
            if request.session.get('roleid') == 4:
                get_teacher_dashboard_details = requests.post(get_teacher_dashboard_details_url,headers=headers, data=data)
                get_teacher_dashboard_details_response = get_teacher_dashboard_details.json()
                return render(request, 'admin/dashboard/teacher_dashboard.html',{"teacher":get_teacher_dashboard_details_response['data']})
            if request.session.get('roleid') == 5:
                data['StudentCode']=request.session.get('PrimaryStudentCode')
                get_announcements_request = requests.post(get_announcements_url,headers=headers, data=data)
                get_announcements_response = get_announcements_request.json()
                return render(request, 'admin/dashboard/parent_dashboard.html',{'announcements':get_announcements_response['data']})
            else:
                get_admin_dashboard_details = requests.post(get_admin_dashboard_details_url,headers=headers, data=data)
                get_admin_dashboard_details_response = get_admin_dashboard_details.json()
                return render(request, 'admin/dashboard/admin_dashboard.html',{"admin":get_admin_dashboard_details_response['data']})
            
            
        else:
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



    

class generate_marksheet(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}


            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            exam_names_list_request = requests.get(exam_names_list_url,headers=headers)
            exam_names_list_response = exam_names_list_request.json()
            return render(request, 'admin/marksheet_master/generate_marksheet.html',{'classes':class_list_response['data'],'academic_years':academic_list_response['data'],'exam_names':exam_names_list_response['data']})

        else:
            return redirect('school:login')




class upload_marksheet(GenericAPIView):
    def get(self,request):
        
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            exam_names_list_request = requests.get(exam_names_list_url,headers=headers)
            exam_names_list_response = exam_names_list_request.json()
            return render(request, 'admin/marksheet_master/upload_marksheet.html',{'classes':class_list_response['data'],'academic_years':academic_list_response['data'],'exam_name':exam_names_list_response['data']})
        else:
            return redirect('school:login')
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            if request.method == 'POST':
                data = request.POST.copy()
                file = request.FILES

                UploadExcelMarkSheet_request = requests.post(UploadExcelMarkSheet_url,data=data,files=file,headers=headers)
                UploadExcelMarkSheet_response = UploadExcelMarkSheet_request.json()
                return HttpResponse(json.dumps(UploadExcelMarkSheet_response), content_type="application/json")





class promote_student(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            exam_names_list_request = requests.get(exam_names_list_url,headers=headers)
            exam_names_list_response = exam_names_list_request.json()
            
            student_list_request = requests.post(search_students_url,headers=headers)
            student_list_response = student_list_request.json()
            
            return render(request, 'admin/marksheet_master/promote_student.html',{'token':tok,'student':student_list_response['data'],'classes':class_list_response['data'],'academic_years':academic_list_response['data'],'exam_name':exam_names_list_response['data']})
        else:
            return redirect('school:login')



class permissions(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/permissions.html',{})
    
    
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)



class reportcard(GenericAPIView):
    def get(self,request,id,classid):
        data = {'studentId':id,'classid':classid}
        GenerateMarkSheet_request = requests.post(GenerateMarkSheet_url,data=data)
        GenerateMarkSheet_response = GenerateMarkSheet_request.json()
        sub_request = requests.get(sub_url)
        sub_response = sub_request.json()
    
        return render(request, 'admin/marksheet_master/reportcard.html',{'AcademicYearId_name':GenerateMarkSheet_response['AcademicYearId_name'],'studentname':GenerateMarkSheet_response['studentname'],'parent_name':GenerateMarkSheet_response['parent_name'],'StudentCode':GenerateMarkSheet_response['StudentCode'],'rollno':GenerateMarkSheet_response['rollno'],'classname':GenerateMarkSheet_response['classname'],'Status':GenerateMarkSheet_response['Status'],'generate':GenerateMarkSheet_response['data'],'subj':sub_response['data']})
    
    
class search_student(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            search_student_request = requests.post(search_student_url, data=data,headers=headers)
            search_student_response = search_student_request.json()
            return HttpResponse(json.dumps(search_student_response), content_type="application/json")
        
    
    
       
    
class search_user(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data = request.data.copy()
            search_user_request = requests.post(search_user_url, data=data,headers=headers)
            search_user_response = search_user_request.json()
            return HttpResponse(json.dumps(search_user_response), content_type="application/json")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    