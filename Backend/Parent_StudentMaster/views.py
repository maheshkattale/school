from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from User.models import User
from User.serializers import UserSerializer,UserlistSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from User.jwt import userJWTAuthentication
from rest_framework import permissions
from .models import *
from .serializers import *
from SchoolMaster.models import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER

frontend_url = 'http://127.0.0.1:8000/'


def createstudentid(schoolcode):
    studentobject = Students.objects.filter(school_code=schoolcode, isActive=True).order_by('-id').first()
    if studentobject is None:
        studentcount = 1
        return f"{schoolcode}/{studentcount:04d}"
    else:
        studentcount = int(studentobject.StudentCode.split('/')[-1]) + 1
        return f"{schoolcode}/{studentcount:04d}"
      



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
            if parentobj is not None :
                parentid = parentobj.id
            
                print("parentiiid",parentid)
                for s in studentlist:
                    print("sssss",s)
                    newstudentcode = createstudentid(schoolcode)
                    print("stucode",newstudentcode)
                    Students.objects.create(ParentId=parentid,StudentName=s['Studentname'],StudentClass_id=s['StudentClass'],DateOfBirth = s['DateOfBirth'],DateofJoining=s['DateofJoining'],school_code=schoolcode,StudentCode=newstudentcode)

            
                #send mail
                subject = "Registration succesful"
                data2 = {"Name": data['Name'],"email":data['Email'],'parentid':parentid,'frontend_url':frontend_url,
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
                    return Response({"data":'',"response": {"n": 1, "msg": "Parent info added successfully","status": "success"}})
                except Exception as e:
                    return Response({'n': 0, 'Msg': 'Email could not be sent', 'Status': 'Failed'})
            else:
                 return Response({'n': 0, 'Msg': 'Parent Not Created', 'Status': 'Failed'})
        
           

class ParentStudentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode)
        parentserializer = UserlistSerializer(Parentobj,many=True)
        for p in parentserializer.data:
            
            studentobj = Students.objects.filter(ParentId = p['id'],isActive=True,school_code=schoolcode)
            studentser =  StudentSerializer(studentobj,many=True)
           
            p['Studentslist'] = studentser.data
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
            stuobj = Students.objects.filter(ParentId = Parentobj.id,isActive=True,school_code=schoolcode)
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
      
        parentobj =  User.objects.filter(id=parentid,isActive= True).first()
        if parentobj is None:
            return Response({"data":'',"response": {"n": 0, "msg": "Parent not found","status": "failure"}})

        parentmailexist = User.objects.filter(email=data['Email'],isActive= True).exclude(id=parentid).first()
        if parentmailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
       
        else:
            parentserializer = UserSerializer(parentobj,data=data,partial=True)
            if parentserializer.is_valid():
                parentserializer.save()

                parentid = parentobj.id

                for s in studentlist:
                    studentdata = {}
                    studentcode = s['studentcode']
                    studentdata['']
                    stuobj = Students.objects.filter(StudentCode=studentcode,isActive=True).first()
                    if stuobj is not None :
                        stuserializer = StudentSerializer(stuobj,data=studentdata,partial=True)
                        if stuserializer.is_valid():
                            stuserializer.save()

                return Response({"data":'',"studentlist":'',"response": {"n": 1, "msg": "parent updated successfully","status": "success"}})
            else:
                return Response({"data":parentserializer.errors,"response": {"n": 0, "msg": "Couldn't Update parent ! ","status": "failure"}})


class getParentStudentbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        parentid = request.data.get('id')
        schoolcode = request.user.school_code
        Parentobj = User.objects.filter(id=parentid,isActive=True,school_code = schoolcode).first()
        if Parentobj is not None:
            serializer = UserlistSerializer(Parentobj)
            studentlist = []
            stuobj = Students.objects.filter(ParentId = Parentobj.id,isActive=True,school_code=schoolcode)
            ser = StudentSerializer(stuobj,many=True)
        
            return Response({"data":serializer.data,"studentlist":ser.data,"response": {"n": 1, "msg": "parent found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "parent not found ","status": "failure"}})



class studentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        studentobj = Students.objects.filter(isActive=True,school_code=schoolcode).order_by('id')
        studentser =  StudentSerializer(studentobj,many=True)
        return Response({"data":studentser.data,"response": {"n": 1, "msg": "students list found successfully","status": "success"}})
    

class studentsbyclasslist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        classname = request.data.get('classname')
        schoolcode = request.user.school_code
        stuobj = Students.objects.filter(StudentClass=classname,isActive=True,school_code=schoolcode)
        ser = StudentSerializer(stuobj,many=True)
        return Response({"data":ser.data,"studentlist":ser.data,"response": {"n": 1, "msg": "students list found successfully","status": "success"}})
      