from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'
exam_type_list_url=frontend_url+'api/MarksheetMaster/List'
add_exam_type_marks_url=frontend_url+'api/MarksheetMaster/add_exam_type_marks'
edit_exam_type_url=frontend_url+'api/MarksheetMaster/update'
delete_exam_type_url=frontend_url+'api/MarksheetMaster/delete'
exam_list_url=frontend_url+'api/MarksheetMaster/Examlist'
delete_exam_list_url=frontend_url+'api/MarksheetMaster/deleteexam'
teacher_list_url=frontend_url+'api/TeacherMaster/list'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'
edit_exam_url=frontend_url+'api/MarksheetMaster/updateexam'
add_exam_url=frontend_url+'api/MarksheetMaster/AddExam'
exam_info_url=frontend_url+'api/MarksheetMaster/Exambyid'
exam_type_marks_list_url=frontend_url+'api/MarksheetMaster/exam_type_marks_list'
subject_list_url=frontend_url+'api/SubjectMaster/List'
delete_exam_type_marks_url=frontend_url+'api/MarksheetMaster/delete_exam_type_marks'
edit_exam_type_marks_url=frontend_url+'api/MarksheetMaster/edit_exam_type_marks'
get_marks_by_exam_type_url=frontend_url+'api/MarksheetMaster/get_marks_by_exam_type'
class exam(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            
            
            exam_list_request = requests.get(exam_list_url,headers=headers)
            exam_list_response = exam_list_request.json()
            return render(request, 'admin/exam/exam_master.html',{'exams':exam_list_response['data']})
        else:
            return redirect('school:login')
        
class edit_exam(GenericAPIView):
    def get(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            exam_type_list_request = requests.get(exam_type_list_url,headers=headers)
            exam_type_list_response = exam_type_list_request.json()
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            teacher_list_request = requests.get(teacher_list_url,headers=headers)
            teacher_list_response = teacher_list_request.json()
            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            data={}
            data['id']=id
            exam_info_request = requests.post(exam_info_url,headers=headers,data=data)
            exam_info_response = exam_info_request.json()
            
            return render(request, 'admin/exam/edit_exam.html',{'exam_types':exam_type_list_response['data'],'classes':class_list_response['data'],'teachers':teacher_list_response['data'],'subjects':subject_list_response['data'],'academics':academic_list_response['data'],'exam':exam_info_response['data']})
        else:
            return redirect('school:login')
        
    def post(self,request,id):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            data['id']=id
            edit_exam_list_request = requests.post(edit_exam_url,data=data,headers=headers)
            edit_exam_list_response = edit_exam_list_request.json()
            return HttpResponse(json.dumps(edit_exam_list_response), content_type="application/json")
        
        
class add_exam(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            exam_type_list_request = requests.get(exam_type_list_url,headers=headers)
            exam_type_list_response = exam_type_list_request.json()
            
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            
            
            teacher_list_request = requests.get(teacher_list_url,headers=headers)
            teacher_list_response = teacher_list_request.json()
            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            academic_list_request = requests.get(academic_list_url,headers=headers)
            academic_list_response = academic_list_request.json()
            
            
            return render(request, 'admin/exam/add_exam.html',{'exam_types':exam_type_list_response['data'],'classes':class_list_response['data'],'teachers':teacher_list_response['data'],'subjects':subject_list_response['data'],'academics':academic_list_response['data']})
        else:
            return redirect('school:login')
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_exam_list_request = requests.post(add_exam_url,data=data,headers=headers)
            add_exam_list_response = add_exam_list_request.json()
            return HttpResponse(json.dumps(add_exam_list_response), content_type="application/json")
        
        
        
        
        
class exam_type(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            exam_type_list_request = requests.get(exam_type_list_url,headers=headers)
            exam_type_list_response = exam_type_list_request.json()
            exam_type_marks_list_request = requests.get(exam_type_marks_list_url,headers=headers)
            exam_type_marks_list_response = exam_type_marks_list_request.json()
            return render(request, 'admin/exam_type/exam_type_master.html',{'exam_types':exam_type_list_response['data'],'exam_type_marks':exam_type_marks_list_response['data']})
        else:
            return redirect('school:login')
        
class add_exam_type_marks(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            add_exam_type_marks_list_request = requests.post(add_exam_type_marks_url,data=data,headers=headers)
            add_exam_type_marks_list_response = add_exam_type_marks_list_request.json()
            return HttpResponse(json.dumps(add_exam_type_marks_list_response), content_type="application/json")
        else:
            return redirect('school:login')
class edit_exam_type_marks(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            edit_exam_type_marks_list_request = requests.post(edit_exam_type_marks_url,data=data,headers=headers)
            edit_exam_type_marks_list_response = edit_exam_type_marks_list_request.json()
            return HttpResponse(json.dumps(edit_exam_type_marks_list_response), content_type="application/json")
        else:
            return redirect('school:login')
class delete_exam_type_marks(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_exam_type_marks_list_request = requests.post(delete_exam_type_marks_url,data=data,headers=headers)
            delete_exam_type_marks_list_response = delete_exam_type_marks_list_request.json()
            return HttpResponse(json.dumps(delete_exam_type_marks_list_response), content_type="application/json")
        else:
            return redirect('school:login')
class delete_exam(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            delete_exam_list_request = requests.post(delete_exam_list_url,data=data,headers=headers)
            delete_exam_list_response = delete_exam_list_request.json()
            return HttpResponse(json.dumps(delete_exam_list_response), content_type="application/json")
        else:
            return redirect('school:login')

class get_marks_by_exam_type(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            get_marks_by_exam_type_request = requests.post(get_marks_by_exam_type_url,data=data,headers=headers)
            get_marks_by_exam_type_response = get_marks_by_exam_type_request.json()
            return HttpResponse(json.dumps(get_marks_by_exam_type_response), content_type="application/json")
        else:
            return redirect('school:login')
        
  
  
  
  
  
  
  
  
  
        
        
        
                
        
        