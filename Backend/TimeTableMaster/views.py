from django.shortcuts import render
from ClassMaster.serializers import *

# Create your views here.
import random

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
from Parent_StudentMaster.serializers import *
from Frontend.school.custom_function import *


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
            user_objs=User.objects.filter(isActive=True)
            serializers=UserlistSerializer(user_objs,many=True)
            return Response({"data":serializers.data,"response": {"n": 1, "msg": "user found successfully","status": "Success"}})
        

# day wise time table
class get_student_time_table_in_week_days(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        school_code = request.user.school_code
        StudentCode=request.POST.get('StudentCode')
        student_obj=Students.objects.filter(StudentCode=StudentCode,school_code=school_code,isActive=True).first()
        print("StudentCode",StudentCode)

        if student_obj is not None:
            student_serializer=StudentSerializer(student_obj)
            ClassId=student_serializer.data['StudentClass']
            current_academic_year=AcademicYear.objects.filter(school_code=school_code,Isdeleted=False,isActive=True).first()
            if current_academic_year is not None:
                data['datelist']=json.loads(data['datelist'])

                days=[]
                for date_str in data['datelist']:
                    day_dict={}
                    day_str=get_day_name(date_str)
                    day_dict[day_str] = []
                    timetabe_obj=TimeTable.objects.filter(school_code=school_code,ClassId=ClassId,AcademicYear=current_academic_year,startdate__lte=date_str,enddate__gte=date_str).order_by('start_time')
                    time_table_serializer=CustomTimeTableSerializer(timetabe_obj,many=True)
                    for period in time_table_serializer.data:
                        if period['Day'] == day_str:
                            period_dict={}
                            period_dict['time']=str(period['start_time'])+' - '+str(period['end_time'])
                            period_dict['Class']=str(period['ClassId'])
                            period_dict['Subject']=str(period['SubjectId'])
                            period_dict['Teacher']=str(period['teacher_name'])
                            day_dict[day_str].append(period_dict)
                    days.append(day_dict)
                return Response({"data":days,"response": {"n": 1, "msg": "Successfully","status": "Success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "Academic year is not active","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Student not found","status": "failed"}})



class get_student_time_table(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        school_code = request.user.school_code
        StudentCode=request.POST.get('StudentCode')
        student_obj=Students.objects.filter(StudentCode=StudentCode,school_code=school_code,isActive=True).first()
        print("StudentCode",StudentCode)

        if student_obj is not None:
            student_serializer=StudentSerializer(student_obj)
            ClassId=student_serializer.data['StudentClass']
            current_academic_year=AcademicYear.objects.filter(school_code=school_code,Isdeleted=False,isActive=True).first()
            if current_academic_year is not None:
                data['datelist']=json.loads(data['datelist'])

                days=[]
                css_classes=["accent-purple-gradient","accent-blue-gradient","accent-cyan-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient","accent-cyan-gradient","accent-green-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient"]
                for date_str in data['datelist']:
                    day_dict={}
                    day_str=get_day_name(date_str)
                    day_dict[day_str] = []
                    timetabe_obj=TimeTable.objects.filter(school_code=school_code,ClassId=ClassId,AcademicYear=current_academic_year,startdate__lte=date_str,enddate__gte=date_str).order_by('start_time')
                    time_table_serializer=CustomTimeTableSerializer(timetabe_obj,many=True)
                    for period in time_table_serializer.data:
                        if period['Day'] == day_str:
                            period_dict={}
                            # print("period",period)
                            period_dict['time']=str(period['start_time'])+' - '+str(period['end_time'])
                            period_dict['Class']=str(period['ClassId'])
                            period_dict['Subject']=str(period['SubjectId'])
                            period_dict['Teacher']=str(period['teacher_name'])
                            subject_last=str(period['SubjectId_id'])[-1]
                            
                            period_dict['css']=css_classes[int(subject_last)]
                            day_dict[day_str].append(period_dict)
                    days.append(day_dict)
                return Response({"data":days,"response": {"n": 1, "msg": "Successfully","status": "Success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "Academic year is not active","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Student not found","status": "failed"}})


class get_class_time_table(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        school_code = request.user.school_code
        classid=request.POST.get('classid')
        class_obj=Class.objects.filter(id=classid,school_code=school_code,isActive=True).first()

        if class_obj is not None:
            class_serializer=ClassSerializer(class_obj)
            ClassId=class_serializer.data['id']
            current_academic_year=AcademicYear.objects.filter(school_code=school_code,Isdeleted=False,isActive=True).first()
            if current_academic_year is not None:
                data['datelist']=json.loads(data['datelist'])
                days=[]
                css_classes=["accent-purple-gradient","accent-blue-gradient","accent-cyan-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient","accent-cyan-gradient","accent-green-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient"]
                for date_str in data['datelist']:
                    day_dict={}
                    day_str=get_day_name(date_str)
                    day_dict[day_str] = []
                    timetabe_obj=TimeTable.objects.filter(school_code=school_code,ClassId=ClassId,AcademicYear=current_academic_year,startdate__lte=date_str,enddate__gte=date_str).order_by('start_time')
                    time_table_serializer=CustomTimeTableSerializer(timetabe_obj,many=True)
                    for period in time_table_serializer.data:
                        if period['Day'] == day_str:
                            period_dict={}
                            # print("period",period)
                            period_dict['time']=str(period['start_time'])+' - '+str(period['end_time'])
                            period_dict['Class']=str(period['ClassId'])
                            period_dict['Subject']=str(period['SubjectId'])
                            period_dict['Teacher']=str(period['teacher_name'])
                            subject_last=str(period['SubjectId_id'])[-1]
                            
                            period_dict['css']=css_classes[int(subject_last)]
                            day_dict[day_str].append(period_dict)
                    days.append(day_dict)
                return Response({"data":days,"response": {"n": 1, "msg": "Successfully","status": "Success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "Academic year is not active","status": "failed"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "class not found","status": "failed"}})



class get_teacher_time_table(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        school_code = request.user.school_code
        TeacherId = request.user.id

        current_academic_year=AcademicYear.objects.filter(school_code=school_code,Isdeleted=False,isActive=True).first()
        if current_academic_year is not None:
            data['datelist']=json.loads(data['datelist'])
            days=[]
            css_classes=["accent-purple-gradient","accent-blue-gradient","accent-cyan-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient","accent-cyan-gradient","accent-green-gradient","accent-orange-gradient","accent-pink-gradient","timetable .accent-red-gradient"]
            for date_str in data['datelist']:
                day_dict={}
                day_str=get_day_name(date_str)
                day_dict[day_str] = []
                timetabe_obj=TimeTable.objects.filter(school_code=school_code,AcademicYear=current_academic_year,startdate__lte=date_str,enddate__gte=date_str,TeacherId=TeacherId).order_by('start_time')
                time_table_serializer=CustomTimeTableSerializer(timetabe_obj,many=True)
                for period in time_table_serializer.data:
                    if period['Day'] == day_str:
                        period_dict={}
                        period_dict['time']=str(period['start_time'])+' - '+str(period['end_time'])
                        period_dict['Class']=str(period['ClassId'])
                        period_dict['Subject']=str(period['SubjectId'])
                        period_dict['Teacher']=str(period['teacher_name'])
                        subject_last=str(period['SubjectId_id'])[-1]
                        
                        period_dict['css']=css_classes[int(subject_last)]
                        day_dict[day_str].append(period_dict)
                days.append(day_dict)
            return Response({"data":days,"response": {"n": 1, "msg": "Successfully","status": "Success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Academic year is not active","status": "failed"}})
        

























































