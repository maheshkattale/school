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
from datetime import datetime, timedelta
from Parent_StudentMaster.models import Students,studentclassLog



class addtimetable(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if request.POST.get('timetablelist') != "":
            timetablelist = json.loads(request.POST.get('timetablelist'))
        else:
            timetablelist = []
        schoolcode = request.user.school_code
        if timetablelist != []:
            for t in timetablelist :
                TimeTable.objects.create(ClassId_id=t['class'],startdate = t['startdate'],enddate=t['enddate'],Day=t['day'],start_time=t['starttime'],end_time = t['endtime'],SubjectId_id=t['subject'],TeacherId = t['teacher'],school_code=schoolcode,AcademicYear_id = t['AcademicYear'])

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
            teacherobj = TeacherSubject.objects.filter(SubjectId = subjectid,isActive=True,school_code=schoolcode)
            teachser = TeacherSubjectSerializer(teacherobj,many=True)
            
            for t in teachser.data:

                tobj = {}
                teacherobj = User.objects.filter(id=t['TeacherId'],isActive=True).first()
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
        return Response({"data":dateser.data,"response": {"n": 1, "msg": "teachers found Successfully","status": "Success"}})
    
    
class timetablelist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        schoolcode = request.user.school_code
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        dateobjs = TimeTable.objects.filter(isActive=True,school_code=schoolcode)

        if startdate is  not None and startdate !="" and enddate is  not None and enddate !="":
            dateobjs = dateobjs.filter(startdate=startdate,enddate=enddate)
            
        dateser = CustomTimeTableSerializer(dateobjs,many=True)

        return Response({"data":dateser.data,"response": {"n": 1, "msg": "time table found Successfully","status": "Success"}})



class checkdaterange(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        schoolcode = request.user.school_code
        newstartdate = request.data.get('startdate')
        newenddate = request.data.get('enddate')
        classid = request.data.get('classid')
        day = request.data.get('day')
        newstarttime =  request.data.get('starttime')
        newendtime = request.data.get('endtime')
        
        
        dateobjs = TimeTable.objects.filter(startdate__lte = newenddate, enddate__gte=newstartdate,ClassId=classid,isActive=True,school_code=schoolcode,start_time__lt = newendtime,Day=day,end_time__gt=newstarttime)
        if dateobjs.exists():
            recordexist = True
            return Response({"data":recordexist,"response": {"n": 1, "msg": "data found Successfully","status": "Success"}})
        else:
           recordexist = False
           return Response({"data":recordexist,"response": {"n": 0, "msg": "data found","status": "failed"}})
       
        

class edittimetable(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        schoolcode = request.user.school_code
        id = request.data.get('id')
        newstartdate = request.data.get('startdate')
        newenddate = request.data.get('enddate')
        classid = request.data.get('classid')
        day = request.data.get('day')
        newstarttime =  request.data.get('starttime')
        newendtime = request.data.get('endtime')
        subject = request.data.get('subject')
        teacherid = request.data.get('teacherid')

        idexist = TimeTable.objects.filter(id=id,isActive=True).first()
        if idexist is not None:
            dateobjs = TimeTable.objects.filter(startdate__lte = newenddate, enddate__gte=newstartdate,ClassId=classid,isActive=True,school_code=schoolcode,start_time__lt = newendtime,Day=day,end_time__gt=newstarttime,SubjectId=subject,TeacherId=teacherid).exclude(id=id)
            if dateobjs.exists():
                return Response({"data":'',"response": {"n": 0, "msg": "record already exist","status": "failed"}})
            else:
                teacheralloted = TimeTable.objects.filter(startdate__lte = newenddate, enddate__gte=newstartdate,isActive=True,school_code=schoolcode,start_time__lt = newendtime,Day=day,end_time__gt=newstarttime,TeacherId=teacherid).exclude(id=id)
                if teacheralloted.exists():
                    return Response({"data":'',"response": {"n": 0, "msg": "Teacher has assigned another class","status": "failed"}})
                else:
                    data['startdate'] = newstartdate
                    data['enddate'] = newenddate
                    data['ClassId'] = classid
                    data['start_time'] = newstarttime
                    data['end_time'] = newendtime
                    data['SubjectId'] = subject
                    data['TeacherId'] = teacherid
                    data['Day']=day
                    dateser = TimeTableSerializer(idexist,data=data,partial=True)
                    if dateser.is_valid():
                        dateser.save()
                        return Response({"data":dateser.data,"response": {"n": 1, "msg": "Timetable Updated Successfully","status": "Success"}})
                    else:
                        return Response({"data":dateser.errors,"response": {"n": 0, "msg": "Couldn't Update Timetable!","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "record not found","status": "failed"}})



class deletetimetable(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        schoolcode = request.user.school_code
        id = request.data.get('id')
        idexist = TimeTable.objects.filter(id=id,isActive=True,school_code=schoolcode).first()
        if idexist is not None:
            data['isActive'] = False
            dateser = TimeTableSerializer(idexist,data=data,partial=True)
            if dateser.is_valid():
                dateser.save()
                return Response({"data":dateser.data,"response": {"n": 1, "msg": "Timetable Record deleted Successfully","status": "Success"}})
            else:
                return Response({"data":dateser.errors,"response": {"n": 0, "msg": "Couldn't delete Timetable record!","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "record not found","status": "failed"}})


class get_ttbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        schoolcode = request.user.school_code
        id = request.data.get('id')
        idexist = TimeTable.objects.filter(id=id,isActive=True,school_code=schoolcode).first()
        if idexist is not None:
            dateser = TimeTableSerializer(idexist)
            return Response({"data":dateser.data,"response": {"n": 1, "msg": "Timetable Record found Successfully","status": "Success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "record not found","status": "failed"}})



# class getttbystudentid(GenericAPIView):
#     authentication_classes=[userJWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self,request):
#         data={}
#         schoolcode = request.user.school_code
#         stuid = request.data.get('stuid')
#         week = request.data.get('week')
#         year = request.data.get('year')

#         startdate = datetime.date.fromisocalendar(year, week, 1)
#         dates = []
#         for i in range(7):
#             day = startdate + datetime.timedelta(days=i)
#             dates.append(day)

#         return Response({"data":dates,"response": {"n": 1, "msg": "Timetable Record found Successfully","status": "Success"}})


class getttbystudentid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        schoolcode = request.user.school_code
        stuid = request.data.get('stuid')
        date = request.data.get('date')

        Academicyearobj = AcademicYear.objects.filter(isActive=True,school_code=schoolcode).first()
        if Academicyearobj is not None:
            academicyearid = Academicyearobj.id
            stuobj = studentclassLog.objects.filter(studentId=stuid,AcademicyearId=academicyearid,school_code=schoolcode).first()
            if stuobj is not None:
                studentclass = stuobj.classid
                ttobjs = TimeTable.objects.filter(ClassId=studentclass,startdate_lte = date ,enddate_gte = date,school_code=schoolcode,isActive=True)
                ttser = CustomTimeTableSerializer(ttobjs,many=True)
                return Response({"data":ttser.data,"response": {"n": 1, "msg": "Timetable Record found Successfully","status": "Success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "student class not found","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "AcademicYear is not active","status": "failed"}})

class get_recipient(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        print("str(request.user.role)",str(request.user.role))
        if str(request.user.role) == "Parent":
            schoolcode = request.user.school_code
            stuid = request.data.get('stuid')
            Academicyearobj = AcademicYear.objects.filter(isActive=True,school_code=schoolcode).first()
            if Academicyearobj is not None:
                academicyearid = Academicyearobj.id
                stuobj = studentclassLog.objects.filter(studentId=stuid,AcademicyearId=academicyearid,school_code=schoolcode).first()
                if stuobj is not None:
                    studentclass = stuobj.classid                
                    ttobjs = TimeTable.objects.filter(ClassId=studentclass,school_code=schoolcode,isActive=True)
                    ttser = CustomTimeTableSerializer(ttobjs,many=True)
                    userlist=[]
                    for i in ttser.data:
                        j={}
                        j['id']=i['TeacherId']
                        j['Username']=i['teacher_name']
                        userlist.append(j)

                    return Response({"data":userlist,"response": {"n": 1, "msg": "Timetable Record found Successfully","status": "Success"}})
                else:
                    return Response({"data":'',"response": {"n": 0, "msg": "student class not found","status": "failed"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "AcademicYear is not active","status": "failed"}})
        else:
            print("byy",)
            user_objs=User.objects.filter(isActive=True)
            serializers=UserlistSerializer(user_objs,many=True)
            # print("serializers",serializers.data)
            return Response({"data":serializers.data,"response": {"n": 1, "msg": "user found successfully","status": "Success"}})