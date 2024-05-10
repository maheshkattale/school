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
from SchoolMaster.serializers import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER
from datetime import datetime
from Frontend.school.static_info import frontend_url,image_url


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
       
        parentmailexist = User.objects.filter(email=data['Email'],isActive= True,school_code=schoolcode).first()
        if parentmailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
        parentmobileexist = User.objects.filter(mobileNumber=data['MobileNumber'],isActive= True,school_code=schoolcode).first()
        if parentmobileexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Mobile Number already exist","status": "failure"}})
        
        else:
            parentcreate = User.objects.create(email=data['Email'],Username = data['Name'], school_code = schoolcode,role_id = 5,password = str(12345),textPassword = str(12345),mobileNumber=data['MobileNumber'],Address = data['Address'])
            
            parentobj = User.objects.filter(email=data['Email']).first()
            if parentobj is not None :
                parentid = parentobj.id
            
                for s in studentlist:
                    date_str = str(s['DateOfBirth'])
                    date_object = datetime.strptime(date_str, "%d-%m-%Y")
                    formatteddob_date = date_object.strftime("%Y-%m-%d")

                    date_str2 = str(s['DateofJoining'])
                    date_object2= datetime.strptime(date_str, "%d-%m-%Y")
                    formattedjoin_date = date_object.strftime("%Y-%m-%d")
                    
                    newstudentcode = createstudentid(schoolcode)
                    Students.objects.create(ParentId=parentid,StudentName=s['Studentname'],StudentClass_id=s['StudentClass'],DateOfBirth = formatteddob_date,DateofJoining=formattedjoin_date,school_code=schoolcode,StudentCode=newstudentcode,BloodGroup=s['BloodGroup'],photo=s['photo'])

            
                #send mail
                subject = "Registration succesful"
                data2 = {"Name": data['Name'],"email":data['Email'],'userid':parentid,'frontend_url':frontend_url,
                         'bestregard_from':'School ERP','phone_no':'0201-890890','school_name':schoolname,
                         
                         
                            "template": 'mails/parent_registration.html'}
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
            for s in studentser.data:
                if s['photo'] != "" and s['photo'] is not None:
                    s['stdimage'] = image_url + str(s['photo'])
                else:
                    s['stdimage'] = image_url + "/static/assets/images/profile.png"
           
            p['Studentslist'] = studentser.data
        return Response({"data":parentserializer.data,"response": {"n": 1, "msg": "Parents list found successfully","status": "success"}})
    

# class getParentStudentbyid(GenericAPIView):
#     authentication_classes=[userJWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self,request):
#         parentid = request.data.get('id')
#         schoolcode = request.user.school_code
#         Parentobj = User.objects.filter(id=parentid,isActive=True,school_code = schoolcode).first()
#         if Parentobj is not None:
#             serializer = UserSerializer(Parentobj)
#             studentlist = []
#             stuobj = Students.objects.filter(ParentId = Parentobj.id,isActive=True,school_code=schoolcode)
#             ser = StudentSerializer(stuobj,many=True)
#             return Response({"data":serializer.data,"studentlist":ser.data,"response": {"n": 1, "msg": "parent found successfully","status": "success"}})
#         else:
#             return Response({"data":'',"response": {"n": 0, "msg": "parent not found ","status": "failure"}})


class updateParentStudent(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
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

        parentmailexist = User.objects.filter(email=data['email'],isActive= True).exclude(id=parentid).first()
        if parentmailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
       
        else:
            parentserializer = UserSerializer(parentobj,data=data,partial=True)
            if parentserializer.is_valid():
                parentserializer.save()
                parentid = parentobj.id

                for s in studentlist:
                 
                    date_str = str(s['DateOfBirth'])
                    date_object = datetime.strptime(date_str, "%d-%m-%Y")
                    formatteddob_date = date_object.strftime("%Y-%m-%d")
                    s['DateOfBirth'] = formatteddob_date

                    date_str2 = str(s['DateofJoining']) 
                    date_object2= datetime.strptime(date_str2, "%d-%m-%Y")
                    formattedjoin_date = date_object2.strftime("%Y-%m-%d")
                    s['DateofJoining'] = formattedjoin_date
                  
                    studentcode = s['StudentCode']
                    if studentcode != '':
                        stuobj = Students.objects.filter(StudentCode=studentcode,isActive=True).first()
                        print()
                        if stuobj is not None :
                            if s['photo'] != "" and s['photo'] is not None:
                                s['photo'] = s['photo']
                            else:
                                s['photo'] = stuobj.photo
                            stuserializer = StudentSerializer(stuobj,data=s,partial=True)
                            if stuserializer.is_valid():
                                stuserializer.save()
                            else:
                                print("stuserializer.errors",stuserializer.errors)
                                # return Response({"data":stuserializer.errors,"response": {"n": 0, "msg": "Couldn't update student ! ","status": "failure"}})
                    else:
                        newstudentcode = createstudentid(schoolcode)
                        Students.objects.create(ParentId=parentid,StudentName=s['StudentName'],StudentClass_id=s['StudentClass'],DateOfBirth = formatteddob_date,DateofJoining=formattedjoin_date,school_code=schoolcode,StudentCode=newstudentcode,BloodGroup=s['BloodGroup'],photo=s['photo'])


                return Response({"data":'',"studentlist":'',"response": {"n": 1, "msg": "parent updated successfully","status": "success"}})
            else:
                return Response({"data":parentserializer.errors,"response": {"n": 0, "msg": "Couldn't Update parent ! ","status": "failure"}})


class getParentStudentbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        parentlist=[]
        parentid = request.data.get('id')
        schoolcode = request.user.school_code
        Parentobj = User.objects.filter(id=parentid,isActive=True,school_code = schoolcode).first()
        if Parentobj is not None:
            serializer = UserlistSerializer(Parentobj)
            serailizer_data = serializer.data
            stucount = Students.objects.filter(ParentId = Parentobj.id,isActive=True,school_code=schoolcode).count()
            serailizer_data.update({"count":stucount})
            
            studentlist = []
            stuobj = Students.objects.filter(ParentId = Parentobj.id,isActive=True,school_code=schoolcode)
            ser = StudentSerializer(stuobj,many=True)
            for s in ser.data:
                date_str = str(s['DateOfBirth'])
                date_object = datetime.strptime(date_str, "%Y-%m-%d")
                formatteddob_date = date_object.strftime("%d-%m-%Y")
                s['DateOfBirth'] = formatteddob_date

                date_str2 = str(s['DateofJoining']) 
                date_object2= datetime.strptime(date_str2, "%Y-%m-%d")
                formattedjoin_date = date_object2.strftime("%d-%m-%Y")
                s['DateofJoining'] = formattedjoin_date

                
                if s['photo'] != "" and s['photo'] is not None:
                    s['photo'] = image_url + str(s['photo'])
                else:
                    s['photo'] = ""

            serailizer_data.update({"studentlist":ser.data})
            return Response({"data":serailizer_data,"response": {"n": 1, "msg": "parent found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "parent not found ","status": "failure"}})



class studentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        studentobj = Students.objects.filter(isActive=True,school_code=schoolcode).order_by('id')
        studentser =  StudentSerializer(studentobj,many=True)
        for s in studentser.data:
            if s['photo'] != "" and s['photo'] is not None:
                s['photo'] = image_url + str(s['photo'])
            else:
                s['photo'] = image_url + "/static/assets/images/profile.png"
        return Response({"data":studentser.data,"response": {"n": 1, "msg": "students list found successfully","status": "success"}})
    

class studentsbyclasslist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        classname = request.data.get('classname')
        schoolcode = request.user.school_code
        stuobj = Students.objects.filter(StudentClass=classname,isActive=True,school_code=schoolcode)
        ser = StudentSerializer(stuobj,many=True)
        for s in ser.data:
            if s['photo'] != "" and s['photo'] is not None:
                s['photo'] = image_url + str(s['photo'])
            else:
                s['photo'] = image_url + "/static/assets/images/profile.png"
        return Response({"data":ser.data,"studentlist":ser.data,"response": {"n": 1, "msg": "students list found successfully","status": "success"}})
      

class studentsbyparentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        parentid = request.data.get('parentid')
        schoolcode = request.user.school_code
        stuobj = Students.objects.filter(ParentId=parentid,isActive=True,school_code=schoolcode).order_by('id')
        ser = StudentSerializer(stuobj,many=True)
        for i in ser.data:
            classobj = Class.objects.filter(id=i['StudentClass'],isActive=True).first()
            if classobj is not None:
                i['classname'] = classobj.ClassName
            else:
                i['classname'] = "--"

            if i['photo'] != "" and i['photo'] is not None:
                i['photo'] = image_url + str(i['photo'])
            else:
                i['photo'] = ""
        return Response({"data":ser.data,"response": {"n": 1, "msg": "students list found successfully","status": "success"}})
    


class bloodgrouplist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        bloodobj = BloodGroup.objects.filter(isActive=True)
        bloodserializer = BloodGroupSerializer(bloodobj,many=True)
        
        return Response({"data":bloodserializer.data,"response": {"n": 1, "msg": "bloodgroup list found successfully","status": "success"}})
    

class deleteParent(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        parentid = data['id']
        parentobj = User.objects.filter(id=parentid,isActive=True).first()
        if parentobj is not None:
            data['isActive'] = False
            serializer = UserSerializer(parentobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()

                studentsobj = Students.objects.filter(ParentId=parentid).update(isActive=False)
                
                return Response({"data":'',"response": {"n": 1, "msg": "Parent Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Parent ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Parent not found ","status": "failure"}})
        


class deleteStudent(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        studentcode = data['studentcode']
        studentobj = Students.objects.filter(StudentCode=studentcode,isActive=True).first()
        if studentobj is not None:
            data['isActive'] = False
            serializer = StudentSerializer(studentobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":'',"response": {"n": 1, "msg": "student Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete student ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student not found ","status": "failure"}})
        

class getstudentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        class_id = data['class']
        ac_yearid = data['yearid']
        schoolcode = request.user.school_code
        studentlist = []

        studentclassLogobj = studentclassLog.objects.filter(AcademicyearId=ac_yearid,classid=class_id,school_code=schoolcode)
        if studentclassLogobj.exists():
            studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
            for s in studentclassser.data:
                stuobj = Students.objects.filter(id=s['studentId'],StudentCode=s['StudentCode'],school_code=schoolcode,isActive=True).first()
                if stuobj is not None:
                    stuser = StudentSerializer(stuobj) 
                    studentlist.append(stuser.data)
        return Response({"data":studentlist,"response": {"n": 1, "msg": "student list found ","status": "success"}})
       

class getstudentidcards(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        idcardlist = []
        data = request.data.copy()
        classid = data['classid']
        ac_year = data['year']
        schoolcode = request.user.school_code
        # studentidlist = json.loads(data['studentlist'])
        if request.POST.get('studentidlist') != "":
            studentidlist = json.loads(request.POST.get('studentidlist'))
        else:
            studentidlist = []

        if studentidlist != "" and  studentidlist != []:
            for i in studentidlist:
                icardobj={}
                studobj = Students.objects.filter(id=i,isActive=True,school_code=schoolcode).first()
                if studobj is not None:
                    icardobj['academic_year'] = ac_year
                    icardobj['studentname'] = studobj.StudentName

                    classobj = Class.objects.filter(id=classid,school_code=schoolcode).first()
                    icardobj['classname'] = classobj.ClassName

                    if studobj.photo != "" and studobj.photo is not None:
                        icardobj['photo'] = image_url + str(studobj.photo)
                    else:
                        icardobj['photo'] = ""

                    icardobj['StudentCode'] = studobj.StudentCode
                    icardobj['DateOfBirth'] = studobj.DateOfBirth

                    schoolobj = School.objects.filter(school_code=schoolcode).first()
                    schoolser = schoolSerializer(schoolobj)
                    icardobj['schooldata'] = schoolser.data

                    parentobj = User.objects.filter(id=studobj.ParentId).first()
                    parentser = UserlistSerializer(parentobj)
                    icardobj['parentinfo'] = parentser.data

                    idcardlist.append(icardobj)

            return Response({"data":idcardlist,"response": {"n": 1, "msg": "student card info found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student list is empty ","status": "failed"}})

