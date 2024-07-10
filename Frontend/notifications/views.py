from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.

check_new_notification_url=frontend_url+'api/NotificationMaster/check_new_notification'
check_new_notification_count_url=frontend_url+'api/NotificationMaster/check_new_notification_count'
user_all_notifications_url=frontend_url+'api/NotificationMaster/user_all_notifications'
# Create your views here.
class check_new_notification(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['student_id']=request.session.get('PrimaryStudentId',None)
            check_new_notification_request = requests.post(check_new_notification_url,headers=headers,data=data)
            check_new_notification_response = check_new_notification_request.json()
            return HttpResponse(json.dumps(check_new_notification_response), content_type="application/json")


class check_new_notification_count(GenericAPIView):


    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['student_id']=request.session.get('PrimaryStudentId',None)
            check_new_notification_count_request = requests.post(check_new_notification_count_url,headers=headers,data=data)
            check_new_notification_count_response = check_new_notification_count_request.json()
            return HttpResponse(json.dumps(check_new_notification_count_response), content_type="application/json")


class all_notifications(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            return render(request, 'admin/notifications_master/notifications.html')
        else:
            return redirect('school:login')
        
        
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data={}
            data['student_id']=request.session.get('PrimaryStudentId',None)
            p = request.POST.get('p')
            print("pp",p)
            user_all_notifications_pagination_url = user_all_notifications_url + "?p=" +str(p)     
            all_notifications_request = requests.post(user_all_notifications_pagination_url,headers=headers,data=data)
            all_notifications_response = all_notifications_request.json()
            return HttpResponse(json.dumps(all_notifications_response), content_type="application/json")


