from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from User.models import User
from User.serializers import UserSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from User.jwt import userJWTAuthentication
from rest_framework import permissions
from .models import *
from .serializers import *
from SchoolMaster.models import *


def createstudentid(schoolname, year, schoolcode):
    school_initials = ''.join([s[0].upper() for s in schoolname.split()])
    studentobject = Students.objects.filter(school_code=schoolcode, isActive=True).order_by('-id').first()
    if studentobject is None:
        studentcount = 1
        return f"{school_initials}/{year % 100:02d}{(year + 1) % 100:02d}/{studentcount:04d}"
    else:
        studentcount = int(studentobject.student_id.split('/')[-1]) + 1
        return f"{school_initials}/{year % 100:02d}{(year + 1) % 100:02d}/{studentcount:04d}"
      



class AddParentStudent(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        studentlist = json.loads(data['studentlist'])
        schoolcode = request.user.school_code

        schoolobj = School.objects.filter(school_code = schoolcode,isActive=True).first()
        if schoolobj is not None:
            schoolname = schoolobj.Name
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "School is Inactive .","status": "failure"}})
       
        parentmailexist = User.objects.filter(email=data['Email'],isActive= True).first()
        if parentmailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
        else:
            parentcreate = User.objects.create(email=data['Email'],Username = data['Name'], school_code = schoolcode,role_id = 5,password = str(12345),textPassword = str(12345),mobileNumber=data['MobileNumber'])

            parentobj = User.objects.filter(email=data['Email']).first()
            parentid = parentobj.id


            print("parentid",parentid)
            for s in studentlist:
                year = str(s['DateofJoining']).split("-")[0]
                newstudentcode = createstudentid(schoolname,year,schoolcode)
                Students.objects.create(ParentId=parentid,StudentName=s['Studentname'],StudentClass=s['StudentClass'],DateOfBirth = s['DateOfBirth'],DateofJoining=s['DateofJoining'],school_code=schoolcode,StudentCode=newstudentcode)

            return Response({"data":'',"response": {"n": 1, "msg": "Parent info added successfully","status": "success"}})
           

class ParentStudentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode)
        parentserializer = UserSerializer(Parentobj,many=True)
        for p in parentserializer.data:
            studentlist = []
            studentobj = Students.objects.filter(ParentId = p['id'],isActive=True,school_code=schoolcode)
            studentser =  StudentSerializer(studentobj,many=True)
           
            studentlist = studentser.data
            
            p['Studentslist'] = studentlist
        return Response({"data":parentserializer.data,"response": {"n": 1, "msg": "Parents list found successfully","status": "success"}})
    

class getParentStudentbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        parentid = request.data.get('id')
        schoolcode = request.user.school_code
        Parentobj = User.objects.filter(id=parentid,isActive=True,school_code = schoolcode).first()
        if Parentobj is not None:
            serializer = UserSerializer(Parentobj)
            studentlist = []
            stuobj = Students.objects.filter(ParentId = p['id'],isActive=True,school_code=schoolcode)
            ser = StudentSerializer(stuobj,many=True)
            return Response({"data":serializer.data,"studentlist":ser.data,"response": {"n": 1, "msg": "parent found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "parent not found ","status": "failure"}})


class updateParentStudent(GenericAPIView):
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        parentid = data['id']
        studentlist = json.loads(data['studentlist'])
        schoolcode = request.user.school_code

        schoolobj = School.objects.filter(school_code = schoolcode,isActive=True).first()
        if schoolobj is not None:
            schoolname = schoolobj.Name
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "School is Inactive .","status": "failure"}})
       
        parentmailexist = User.objects.filter(email=data['Email'],isActive= True).exclude(id=parentid).first()
        if parentmailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
        else:
            return Response({"data":'',"studentlist":'',"response": {"n": 1, "msg": "parent found successfully","status": "success"}})