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
teacher_classes_list_url=frontend_url+'api/ClassMaster/teacher_classes_list'
get_class_attendance_by_date_url=frontend_url+'api/AttendanceMaster/get_class_attendance_by_date'
mark_class_attendance_url=frontend_url+'api/AttendanceMaster/mark_class_attendance'
# Create your views here.

class class_attendance(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            teacher_classes_list_request = requests.get(teacher_classes_list_url,headers=headers)
            teacher_classes_list_response = teacher_classes_list_request.json()
            print("teacher_classes_list_response['data']",teacher_classes_list_response['data'])
            return render(request, 'admin/attendance/class_attendance.html',{
                'classes':teacher_classes_list_response['data']
                })
        else:
            return redirect('school:login')
class get_class_attendance_by_date(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            get_class_attendance_by_date_request = requests.post(get_class_attendance_by_date_url,headers=headers,data=data)
            get_class_attendance_by_date_response = get_class_attendance_by_date_request.json()
            return HttpResponse(json.dumps(get_class_attendance_by_date_response), content_type="application/json")

        else:
            return redirect('school:login')
class mark_class_attendance(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            mark_class_attendance_request = requests.post(mark_class_attendance_url,headers=headers,data=data)
            mark_class_attendance_response = mark_class_attendance_request.json()
            print("mark_class_attendance_response['data']",mark_class_attendance_response['data'])
            return HttpResponse(json.dumps(mark_class_attendance_response), content_type="application/json")

        else:
            return redirect('school:login')





