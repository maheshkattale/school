from django.shortcuts import render
import json
from rest_framework.generics import GenericAPIView
from User.models import *
from User.serializers import *
from SchoolMaster.serializers import *
from rest_framework.authentication import (BaseAuthentication,get_authorization_header)
from rest_framework import permissions
from User.jwt import userJWTAuthentication
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER
from Frontend.school.static_info import frontend_url,image_url
from .models import *
from .serializers import *

class mark_read_all_notifications(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        to_user = request.user.id
        school_code = request.user.school_code
        student_id = request.POST.get('student_id')
        if student_id is not None and student_id !='':
            Mark_Read_obj=NotificationMaster.objects.filter(to_user=to_user,student_id=student_id,school_code=school_code).update(notification_read=True)
        else:
            Mark_Read_obj=NotificationMaster.objects.filter(to_user=to_user,school_code=school_code).update(notification_read=True)
        return Response({"data":'',"response": {"n": 1, "msg": "Notifications marked as read","status": "success"}})
    
class check_new_notification(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        to_user = request.user.id
        school_code = request.user.school_code
        student_id = request.POST.get('student_id')
        if student_id is not None and student_id !='':
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,to_user_studentid=student_id,school_code=school_code)[:5]
        else:
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,school_code=school_code)[:5]
        if notifications_obj.exists():
            serializer=CustomNotificationMasterSerializer(notifications_obj,many=True)
            newlist=serializer.data
            mark_read=NotificationMaster.objects.filter(to_user=to_user,school_code=school_code).update(notification_read=True)
            return Response({"data":newlist,"response": {"n": 1, "msg": "New Notifications ","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No Notifications ","status": "faliure"}})
            
class check_new_notification_count(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        to_user = request.user.id
        school_code = request.user.school_code
        student_id = request.POST.get('student_id')
        if student_id is not None and student_id !='':
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,notification_read=False,to_user_studentid=student_id,school_code=school_code)
        else:
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,notification_read=False,school_code=school_code)
        if notifications_obj.exists():
            return Response({"data":notifications_obj.count(),"response": {"n": 1, "msg": "New Notifications ","status": "success"}})
        else:
            return Response({"data":notifications_obj.count(),"response": {"n": 0, "msg": "No Notifications ","status": "faliure"}})
      
class user_all_notifications(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=CustomPagination
    
    def post(self,request):
        to_user = str(request.user.id)
        school_code = request.user.school_code
        student_id = request.POST.get('student_id')
        if student_id is not None and student_id !='':
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,to_user_studentid=student_id,school_code=school_code)
        else:
            notifications_obj=NotificationMaster.objects.filter(to_user=to_user,school_code=school_code)
        if notifications_obj.exists():
            page = self.paginate_queryset(notifications_obj)               
            serializer=CustomNotificationMasterSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)  
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No Notifications ","status": "faliure"}})
            

            
       