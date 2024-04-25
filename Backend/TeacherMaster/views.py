

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
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

frontend_url = 'http://127.0.0.1:8000/'

class AddTeacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        subjects = json.loads(data['subjects'])
        schoolcode = request.user.school_code
        teacherexist = User.objects.filter(Username=data['Name'],isActive= True).first()
        if teacherexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher Name already exist","status": "failure"}})
        
        teacheremailexist = User.objects.filter(email=data['Email'],isActive= True).first()
        if teacheremailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
        teachermobileexist = User.objects.filter(mobileNumber=data['MobileNumber'],isActive= True).first()
        if teachermobileexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Mobile Number already exist","status": "failure"}})
        
        else:
            teachercreate = User.objects.create(email=data['Email'],Username = data['Name'], school_code = schoolcode,role_id = 4,password = str(12345),textPassword = str(12345),designation_id=data['Designation'],mobileNumber=data['MobileNumber'],joiningDate=data['joiningDate'])

            teacherobj = User.objects.filter(email=data['Email'],isActive=True).first()
            if teacherobj is not None :
                teacherid = teacherobj.id

                for s in subjects:
                    TeacherSubject.objects.create(TeacherId=str(teacherid),SubjectId_id=s)

                #send mail
                subject = "Registration succesful"
                data2 = {"Name": data['Name'],"email":data['Email'],'teacherid':teacherid,'frontend_url':frontend_url,
                            "template": 'mails/school_registration.html'}
                message = render_to_string(
                        data2['template'], data2)
                # send_mail(data2, message)
                try:
                    msg = EmailMessage(
                        subject,
                        message,
                        EMAIL_HOST_USER,
                        [data['Email']],
                    )
                    msg.content_subtype = "html"
                    m = msg.send()
                    if m:
                        print(m)
                    data['n'] = 1
                    data['Msg'] = 'Email has been sent'
                    data['Status'] = "Success"
                    return Response({"data":'',"response": {"n": 1, "msg": "Teacher added successfully","status": "success"}})
                except Exception as e:
                    return Response({'n': 0, 'Msg': 'Email could not be sent', 'Status': 'Failed'})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "Teacher not created","status": "failure"}})



class Teacherlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        teacherobj = User.objects.filter(isActive=True,role_id=4,school_code = schoolcode)
        teacherserializer = UserlistSerializer(teacherobj,many=True)
        for t in teacherserializer.data:
            subjectlist = []
            subjectobj = TeacherSubject.objects.filter(TeacherId = t['id'],isActive=True)
            subjectser =  TeacherSubjectSerializer(subjectobj,many=True)
            for s in subjectser.data:
                subdict={}
                subobj = Subject.objects.filter(id=s['SubjectId'],isActive=True).first()
                if subobj is not None:
                    subdict['subid'] = s['SubjectId']
                    subdict['subjectname'] = subobj.SubjectName
                    subjectlist.append(subdict)
            
            t['Subjects'] = subjectlist
        return Response({"data":teacherserializer.data,"response": {"n": 1, "msg": "Teachers list found successfully","status": "success"}})
    

class getTeacherbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id = request.data.get('id')
        teacherobj = User.objects.filter(id=id,isActive=True).first()
        if teacherobj is not None:
            serializer = UserSerializer(teacherobj)
            subjectlist = []
            subjectidlist = []
            teachersubjectobj = TeacherSubject.objects.filter(TeacherId=teacherobj.id,isActive=True)
            ser = TeacherSubjectSerializer(teachersubjectobj,many=True)
            for t in ser.data:
                subdict={}
                subobj = Subject.objects.filter(id=t['SubjectId'],isActive=True).first()
                if subobj is not None:
                    subdict['subid'] = t['SubjectId']
                    subdict['subjectname'] = subobj.SubjectName
                    subjectlist.append(subdict)
                    subjectidlist.append(t['SubjectId'])
            return Response({"data":serializer.data,"subjectlist":subjectlist,'subjectidlist':subjectidlist,"response": {"n": 1, "msg": "Teacher found successfully","status": "success"}})
        else:
            return Response({"data":'','subjectlist':[],'subjectidlist':[],"response": {"n": 0, "msg": "Teacher not found ","status": "failure"}})


class deleteTeacher(GenericAPIView):
    def post(self,request):
        data = request.data.copy()
        teacherid = data['id']
        Teacherobj = User.objects.filter(id=teacherid,isActive=True).first()
        if teacherid is not None:
            data['isActive'] = False
            serializer = UserSerializer(Teacherobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()

                subjectsobj = TeacherSubject.objects.filter(TeacherId=teacherid).update(isActive=False)
                
                return Response({"data":'',"response": {"n": 1, "msg": "Teacher Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Teacher ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher not found ","status": "failure"}})



class UpdateTeacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        subjects = json.loads(data['subjects'])
        schoolcode = request.user.school_code
        teacher_obj = User.objects.filter(id=data['id'],isActive= True).first()
        if teacher_obj is not None:
            
            teacherexist = User.objects.filter(Username=data['Username'],isActive= True).exclude(id=data['id']).first()
            if teacherexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Teacher Name already exist","status": "failure"}})
            
            teacheremailexist = User.objects.filter(email=data['email'],isActive= True).exclude(id=data['id']).first()
            if teacheremailexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
            
            teachermobileexist = User.objects.filter(mobileNumber=data['mobileNumber'],isActive= True).exclude(id=data['id']).first()
            if teachermobileexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Mobile Number already exist","status": "failure"}})
            
            else:
                serializer=UserSerializer(teacher_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    delete_subject=TeacherSubject.objects.filter(TeacherId=str(serializer.data['id'])).delete()
                    for s in subjects:
                        subject_obj=TeacherSubject.objects.create(TeacherId=str(serializer.data['id']),SubjectId_id=s)
                            
                    return Response({"data":'',"response": {"n": 1, "msg": "Teacher updated successfully","status": "success"}})
                else:
                    first_key, first_value = next(iter(serializer.errors.items()))
                    return Response({"data":'',"response": {"n": 0, "msg": first_key +' ' +first_value[0],"status": "failure"}})

        else:
            
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher not found","status": "failure"}})

