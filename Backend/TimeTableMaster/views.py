from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
from TeacherMaster.models import TeacherSubject
from TeacherMaster.serializers import *
from SubjectMaster.serializers import SubjectSerializer
from User.models import User
from User.serializers import UserSerializer,UserlistSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from User.jwt import userJWTAuthentication
from rest_framework import permissions
from .models import *
from .serializers import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER



class addtimetable(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        print("res",request.POST)
        if request.POST.get('timetablelist') != "":
            timetablelist = json.loads(request.POST.get('timetablelist'))
        else:
            timetablelist = []
        print("timetablelist",timetablelist)
        schoolcode = request.user.school_code


        if timetablelist != []:
            for t in timetablelist :
                TimeTable.objects.create(ClassId_id=t['class'],startdate = t['startdate'],enddate=t['enddate'],Day=t['day'],start_time=t['starttime'],end_time = t['endtime'],SubjectId_id=t['subject'],TeacherId = t['teacher'],school_code=schoolcode)

            return Response({"data":'',"response": {"n": 1, "msg": "TimeTable Added Successfully","status": "Success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "TimeTable list is empty","status": "failed"}})
        




class getteachersfromsub(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        subjectid = request.data.get('subject')
        teacherlist = []
        schoolcode = request.user.school_code
        if subjectid is not None or subjectid != '':
            teacherobj = TeacherSubject.objects.filter(SubjectId_id = subjectid,isActive=True,school_code=schoolcode)
            teachser = TeacherSubjectSerializer(teacherobj,many=True)
            for t in teachser.data:
                tobj = {}
                teacherobj = User.objects.filter(id=t['id'],isActive=True).first()
                if teacherobj is not None:
                    tobj['teacherid'] = teacherobj.id
                    tobj['teachername'] = teacherobj.Username

                    teacherlist.append(tobj)

            return Response({"data":teacherlist,"response": {"n": 1, "msg": "teachers found Successfully","status": "Success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "sujectid not found","status": "failed"}})



class daterangelist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        dateobjs = TimeTable.objects.filter(isActive=True,school_code=schoolcode)
        dateser = TimeTableSerializer(dateobjs,many=True)
        return Response({"data":dateser,"response": {"n": 1, "msg": "teachers found Successfully","status": "Success"}})
    
class timetablelist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        schoolcode = request.user.school_code
        dateobjs = TimeTable.objects.filter(isActive=True,school_code=schoolcode)
        dateser = TimeTableSerializer(dateobjs,many=True)
        return Response({"data":dateser,"response": {"n": 1, "msg": "teachers found Successfully","status": "Success"}})