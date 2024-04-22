

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
from SubjectMaster.serializers import SubjectSerializer
from User.models import User
from User.serializers import UserSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from User.jwt import userJWTAuthentication
from rest_framework import permissions
from .models import *
from .serializers import *




class AddTeacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        subjects = json.loads(data['Members'])
        print("subjects",subjects,type(subjects))
        schoolcode = request.user.school_code
        print("sss",schoolcode)
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
            teachercreate = User.objects.create(email=data['Email'],Username = data['Name'], school_code = schoolcode,role_id = 4,password = str(12345),textPassword = str(12345),Designation_id=data['Designation'],mobileNumber=data['MobileNumber'])

            teacherobj = User.objects.filter(email=data['Email']).first()
            teacherid = teacherobj.id

            print("teacherid",teacherid)
            for s in subjects:
                TeacherSubject.objects.create(TeacherId=teacherid,SubjectId_id=s)

            return Response({"data":'',"response": {"n": 1, "msg": "Subject added successfully","status": "success"}})
           


class Teacherlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        teacherobj = User.objects.filter(isActive=True,role_id=4,school_code = schoolcode)
        teacherserializer = UserSerializer(teacherobj,many=True)
        for t in teacherserializer.data:
            subjectlist = []
            subjectobj = TeacherSubject.objects.filter(TeacherId = t['id'],isActive=True)
            subjectser =  TeacherSubjectSerializer(subjectobj,many=True)
            for s in subjectser.data:
                subjectlist.append(s['SubjectId'])
            
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
            teachersubjectobj = TeacherSubject.objects.filter(TeacherId=teacherobj.id,isActive=True)
            ser = TeacherSubjectSerializer(teachersubjectobj,many=True)
            for t in ser.data:
                subjectlist.append(t['SubjectId'])

            return Response({"data":serializer.data,"subjectlist":subjectlist,"response": {"n": 1, "msg": "Teacher found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher not found ","status": "failure"}})


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
                
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Teacher Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Teacher ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher not found ","status": "failure"}})
