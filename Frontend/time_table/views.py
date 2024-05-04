from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url

subject_list_url=frontend_url+'api/SubjectMaster/List'
teacher_list_url=frontend_url+'api/TeacherMaster/list'
class_list_url=frontend_url+'api/ClassMaster/List'
timetable_list_url=frontend_url+'api/TimeTableMaster/timetablelist'
timetable_add_url=frontend_url+'api/TimeTableMaster/Add'
timetable_delete_url=frontend_url+'api/TimeTableMaster/deletetimetable'
timetable_by_id_url=frontend_url+'api/TimeTableMaster/get_ttbyid'
timetable_edit_url=frontend_url+'api/TimeTableMaster/edittimetable'
get_teacher_by_subject_url=frontend_url+'api/TimeTableMaster/getteachersfromsub'
timetable_dates_ranges_url=frontend_url+'api/TimeTableMaster/daterangelist'


class time_table_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/time_table_master.html',{})
    
class add_time_table(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}

            subject_list_request = requests.get(subject_list_url,headers=headers)
            subject_list_response = subject_list_request.json()
            teacher_list_request = requests.get(teacher_list_url,headers=headers)
            teacher_list_response = teacher_list_request.json()
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            timetable_dates_ranges_request = requests.get(timetable_dates_ranges_url,headers=headers)
            timetable_dates_ranges_response = timetable_dates_ranges_request.json()
            timetable_list_request = requests.post(timetable_list_url,headers=headers)
            timetable_list_response = timetable_list_request.json()
            print("timetable_list_response",timetable_list_response)
            
            context={
                'subjects':subject_list_response['data'],
                'teachers':teacher_list_response['data'],
                'timetable_dates_ranges':timetable_dates_ranges_response['data'],
                'classes':class_list_response['data'],
                'timetableslist':timetable_list_response['data'],
            }
            return render(request, 'admin/time_table_master/add_time_table.html',context)
        else:
            return redirect('school:login')
    def post(self,request):
        
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            
            timetable_add_request = requests.post(timetable_add_url,headers=headers,data=data)
            timetable_add_response = timetable_add_request.json()
            return HttpResponse(json.dumps(timetable_add_response), content_type="application/json")
        
        
class edit_timetable(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/edit_time_table.html',{})
    def post(self,request):
        
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            print("data",data)
            timetable_edit_request = requests.post(timetable_edit_url,headers=headers,data=data)
            timetable_edit_response = timetable_edit_request.json()
            return HttpResponse(json.dumps(timetable_edit_response), content_type="application/json")
class delete_timetable(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            timetable_delete_request = requests.post(timetable_delete_url,headers=headers,data=data)
            timetable_delete_response = timetable_delete_request.json()
            return HttpResponse(json.dumps(timetable_delete_response), content_type="application/json")
class get_timetable_by_id(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            timetable_by_id_request = requests.post(timetable_by_id_url,headers=headers,data=data)
            timetable_by_id_response = timetable_by_id_request.json()
            return HttpResponse(json.dumps(timetable_by_id_response), content_type="application/json")
class get_teacher_by_subject(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            get_teacher_by_subject_request = requests.post(get_teacher_by_subject_url,headers=headers,data=data)
            get_teacher_by_subject_response = get_teacher_by_subject_request.json()
            return HttpResponse(json.dumps(get_teacher_by_subject_response), content_type="application/json")
        
        