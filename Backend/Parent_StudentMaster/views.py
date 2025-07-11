from django.shortcuts import render
from django.db.models import F

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
from MarksheetMaster.models import *
from SchoolMaster.serializers import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER
from datetime import datetime
from Frontend.school.static_info import frontend_url,image_url
from Frontend.school.custom_function import *
from tablib import Dataset
from rest_framework import generics, permissions, status


def createstudentid(schoolcode):
    studentobject = Students.objects.filter(school_code=schoolcode, isActive=True).order_by('-id').first()
    if studentobject is None:
        studentcount = 1
        return f"{schoolcode}/{studentcount:04d}"
    else:
        studentcount = int(studentobject.StudentCode.split('/')[-1]) + 1
        return f"{schoolcode}/{studentcount:04d}"
      
def dateformat(datetoformat):
    x = datetime.strptime(datetoformat, '%Y-%m-%d')
    changeddate = x.strftime('%d-%b-%Y')
    return str(changeddate)


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
                    s['ParentId']=str(parentid)
                    s['StudentName']=s['Studentname']
                    s['StudentClass_id']=s['StudentClass']
                    s['DateOfBirth']=formatteddob_date
                    s['DateofJoining']=formattedjoin_date
                    s['school_code']=schoolcode
                    s['StudentCode']=newstudentcode
                    if 'photo' in s.keys():
                        s['photo']=s['photo']
                    s['DateofJoining']=formattedjoin_date
                    s['RollNo'] = s['RollNo']
                    student_serializer=StudentSerializer(data=s)
                    if student_serializer.is_valid():
                        student_serializer.save()
                        
                                
                            
                        AcademicYear_obj = AcademicYear.objects.filter(Isdeleted=False,isActive=True,school_code=schoolcode).first()
                        if AcademicYear_obj is not None:
                            class_data={}
                            class_data['AcademicyearId']=AcademicYear_obj.id
                            class_data['studentId']=student_serializer.data['id']
                            class_data['StudentCode']=student_serializer.data['StudentCode']
                            class_data['classid']=student_serializer.data['StudentClass']
                            class_data['school_code']=schoolcode
                            class_data['RollNo'] = student_serializer.data['RollNo']
                            student_class_serializer=studentclassLogserializer(data=class_data)
                            if student_class_serializer.is_valid():
                                student_class_serializer.save()
                            else:
                                print("student_class_serializer error",student_class_serializer.errors)
                        else:
                            print("AcademicYear_obj error")
                    else:
                        print("student error",student_serializer.errors)
                        
                            
                            
            
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
    pagination_class=CustomPagination
    
    def get(self,request):
        schoolcode = request.user.school_code
        search = request.GET.get('search')
        Parentobj = ''
        if search is not None and search !="":
            Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode,Username__icontains=search)
        else:
            Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode)
        if Parentobj.exists():
            page = self.paginate_queryset(Parentobj)               
            parentserializer = UserlistSerializer(page,many=True)
            return self.get_paginated_response(parentserializer.data) 
        else:
                   
            return Response({"data":[],"response": {"n": 0, "msg": "Parents list not found ","status": "failure"}})
        
    def post(self,request):
        schoolcode = request.user.school_code
        search = request.POST.get('search')
        Parentobj = ''
        if search is not None and search !="":
            Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode,Username=search)
        else:
            Parentobj = User.objects.filter(isActive=True,role_id=5,school_code = schoolcode)
        if Parentobj.exists():
            page = self.paginate_queryset(Parentobj)               
            parentserializer = UserlistSerializer(page,many=True)
            return self.get_paginated_response(parentserializer.data) 
        else:
                   
            return Response({"data":[],"response": {"n": 0, "msg": "Parents list not found ","status": "failure"}})
    
    
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

        parentmailexist = User.objects.filter(email=data['email'],isActive=True,school_code=schoolcode).exclude(id=parentid).first()
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
                        if stuobj is not None :
     
                            stuserializer = StudentSerializer(stuobj,data=s,partial=True)
                            if stuserializer.is_valid():
                                stuserializer.save()
                                AcademicYear_obj = AcademicYear.objects.filter(Isdeleted=False,isActive=True,school_code=schoolcode).first()
                                if AcademicYear_obj is not None:
                                    class_data={}
                                    class_data['AcademicyearId']=AcademicYear_obj.id
                                    class_data['studentId']=stuserializer.data['id']
                                    class_data['StudentCode']=stuserializer.data['StudentCode']
                                    class_data['classid']=stuserializer.data['StudentClass']
                                    class_data['school_code']=schoolcode
                                    class_data['RollNo']=stuserializer.data['RollNo']
                                    class_lof_obj=studentclassLog.objects.filter(studentId=class_data['studentId'],StudentCode=class_data['StudentCode'],AcademicyearId=class_data['AcademicyearId']).first()
                                    if class_lof_obj is not None:
                                        student_class_serializer=studentclassLogserializer(class_lof_obj,data=class_data)
                                    else:
                                        student_class_serializer=studentclassLogserializer(data=class_data)
                                    if student_class_serializer.is_valid():
                                        student_class_serializer.save()
                                    else:
                                        print("student_class_serializer error",student_class_serializer.errors)
                                else:
                                    print("AcademicYear_obj error")
                                
                                
                                
                                
                            else:
                                print("stuserializer.errors",stuserializer.errors)
                                # return Response({"data":stuserializer.errors,"response": {"n": 0, "msg": "Couldn't update student ! ","status": "failure"}})
                    else:
                        newstudentcode = createstudentid(schoolcode)
                        s['ParentId']=str(parentid)
                        s['DateOfBirth']=formatteddob_date
                        s['DateofJoining']=formattedjoin_date
                        s['school_code']=schoolcode
                        s['StudentCode']=newstudentcode
                        newstudent_serializer = StudentSerializer(data=s)
                        if newstudent_serializer.is_valid():
                            newstudent_serializer.save()
                            AcademicYear_obj = AcademicYear.objects.filter(Isdeleted=False,isActive=True,school_code=schoolcode).first()
                            if AcademicYear_obj is not None:
                                class_data={}
                                class_data['AcademicyearId']=AcademicYear_obj.id
                                class_data['studentId']=newstudent_serializer.data['id']
                                class_data['StudentCode']=newstudent_serializer.data['StudentCode']
                                class_data['classid']=newstudent_serializer.data['StudentClass']
                                class_data['school_code']=schoolcode
                                student_class_serializer=studentclassLogserializer(data=class_data)
                                if student_class_serializer.is_valid():
                                    student_class_serializer.save()
                                else:
                                    print("student_class_serializer error",student_class_serializer.errors)
                            else:
                                print("AcademicYear_obj error")
                            
                            
                            
                        else:
                            print("newstudent_serializer.errors",newstudent_serializer.errors)
                            first_key, first_value = next(iter(newstudent_serializer.errors.items()))
                            
                            return Response({"data":'',"studentlist":'',"response": {"n": 1, "msg":first_key + " : "+ first_value[0],"status": "failed"}})
                            
        
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
                    s['photo'] = s['photo']
                else:
                    s['photo'] = ""


                bloodobj = BloodGroup.objects.filter(id=s['BloodGroup']).first()
                s['BloodGroup'] = bloodobj.Groupname

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

            bloodobj = BloodGroup.objects.filter(id=s['BloodGroup']).first()
            s['BloodGroup'] = bloodobj.Groupname


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
                i['photo'] = i['photo']
            else:
                i['photo'] = ""

            if starts_with(i['photo'],'data:application/pdf'):
                i['iframes']=True
            else:
                i['iframes']=False

            bloodobj = BloodGroup.objects.filter(id=i['BloodGroup']).first()
            i['BloodGroup'] = bloodobj.Groupname

            # x = datetime.strptime(i['DateOfBirth'], '%Y-%m-%d')
            # i['DateOfBirth']= x.strftime('%d-%b-%Y')


            i['DateOfBirth']= dateformat(i['DateOfBirth'])

            i['DateofJoining'] = dateformat(i['DateofJoining'])

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

class update_student(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        id = data['id']
        studentobj = Students.objects.filter(id=id,isActive=True).first()
        if studentobj is not None:
            serializer = StudentSerializer(studentobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":'',"response": {"n": 1, "msg": "Student updated successfully","status": "success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":serializer.errors,"response": {"n": 0, "msg":str(first_key) +' : '+str(first_value[0]),"status": "failure"}})
            
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student not found ","status": "failure"}})
        
class getstudentlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        
        schoolcode = request.user.school_code
        studentlist = []
                
        studentclassLogobj = studentclassLog.objects.filter(school_code=schoolcode)
        if 'class' in request.data.keys():
            if request.data.get('class') is not None and request.data.get('class') !='':
                class_id = data['class']
                studentclassLogobj = studentclassLogobj.filter(classid=class_id)
                
        if 'yearid' in request.data.keys():
            if request.data.get('yearid') is not None and request.data.get('yearid') !='':
                ac_yearid = data['yearid']
                studentclassLogobj = studentclassLogobj.filter(AcademicyearId=ac_yearid)
                
        if 'promote_classid' in request.data.keys():
            if request.data.get('promote_classid') is not None and request.data.get('promote_classid') !='':
                proid = data['promote_classid']
                studentclassLogobj = studentclassLogobj.filter(promote_class=proid)
        
        if studentclassLogobj.exists():
            studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
            for s in studentclassser.data:
            
                stuobj = Students.objects.filter(id=s['studentId'],StudentCode=s['StudentCode'],school_code=schoolcode,isActive=True).first()
                if stuobj is not None:
                    stuser = StudentSerializer1(stuobj) 
                    details = []
                    for t in [stuser.data]:
                        t['classid'] = s['classid']
                        # t['exam_name'] = s['Exam']
                        details.append(t)
                    studentlist.append(details[0])
        return Response({"data":studentlist,"response": {"n": 1, "msg": "Data found successfully","status": "success"}})

class search_student_by_class_and_year(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        schoolcode = request.user.school_code
        studentlist = []
        studentclassLogobj = studentclassLog.objects.filter(school_code=schoolcode).order_by('AcademicyearId')
        if 'class' in request.data.keys():
            if request.data.get('class') is not None and request.data.get('class') !='':
                class_id = data['class']
                studentclassLogobj = studentclassLogobj.filter(classid=class_id)
                
        if 'yearid' in request.data.keys():
            if request.data.get('yearid') is not None and request.data.get('yearid') !='':
                ac_yearid = data['yearid']
                studentclassLogobj = studentclassLogobj.filter(AcademicyearId=ac_yearid)
                

        if studentclassLogobj.exists():
            studentclassser = custom_studentclassLogserializer(studentclassLogobj,many=True)
            studentlist=studentclassser.data
            for s in studentlist:
                student_obj=Students.objects.filter(StudentCode=s['StudentCode'],isActive=True,school_code=schoolcode).first()
                if student_obj is not None:
                    student_serilzer=StudentSerializer(student_obj)
                    s['student_details']=student_serilzer.data




            return Response({"data":studentlist,"response": {"n": 1, "msg": "Students found successfully","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No student found ","status": "failure"}})

class getstudentidcards(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        idcardlist = []
        data = request.data.copy()

        schoolcode = request.user.school_code
        # studentidlist = json.loads(data['studentlist'])
        if request.POST.get('studentidlist') != "":
            studentidlist = json.loads(request.POST.get('studentidlist'))
        else:
            studentidlist = []

        if studentidlist != "" and  studentidlist != []:
            for i in studentidlist:
                icardobj={}
                check_class=studentclassLog.objects.filter(studentId=i['studentid'],classid=i['classid'],AcademicyearId=i['AcademicyearId'],isActive=True,school_code=schoolcode).first()
                if  check_class is not None:
                    classlog_serializer=custom_studentclassLogserializer(check_class)
                    studobj = Students.objects.filter(id=i['studentid'],isActive=True,school_code=schoolcode).first()
                    if studobj is not None:
                        srudent_serializer=CustomStudentSerializer(studobj)
                        icardobj['academic_year'] = classlog_serializer.data['AcademicyearId']
                        icardobj['studentname'] = srudent_serializer.data['StudentName']
                        classobj = Class.objects.filter(id=i['classid'],school_code=schoolcode).first()
                        if classobj is not None:
                            icardobj['classname'] = classobj.ClassName
                        else:
                            icardobj['classname'] = ''

                        if srudent_serializer.data['photo'] != "" and srudent_serializer.data['photo'] is not None:
                                
                            
                            if starts_with(srudent_serializer.data['photo'],'data:application/pdf'):
                                icardobj['photo'] = '<iframe width="140" src="'+srudent_serializer.data['photo']+'"  frameborder="0" scrolling="no" style="overflow:hidden;" allowfullscreen></iframe>'
                            else:
                                icardobj['photo'] = '<img src="'+srudent_serializer.data['photo']+'" width="140"/>'

                

                        else:
                            icardobj['photo'] = ""

                        icardobj['StudentCode'] = srudent_serializer.data['StudentCode']
                        icardobj['DateOfBirth'] = srudent_serializer.data['DateOfBirth']

                        schoolobj = School.objects.filter(school_code=schoolcode).first()
                        if schoolobj is not None:
                            schoolser = schoolSerializer(schoolobj)
                            icardobj['schooldata'] = schoolser.data
                        else:
                            icardobj['schooldata'] = []

                        parentobj = User.objects.filter(id=srudent_serializer.data['ParentId']).first()
                        if parentobj is not None:
                            parentser = UserlistSerializer(parentobj)
                            icardobj['parentinfo'] = parentser.data
                        else:
                            icardobj['parentinfo'] = []

                        idcardlist.append(icardobj)

            return Response({"data":idcardlist,"response": {"n": 1, "msg": "student card info found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student list is empty ","status": "failed"}})

class search_student_by_class_of_currentyear(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        school_code = request.user.school_code
        studentlist = []
        studentclassLogobj = studentclassLog.objects.filter(school_code=school_code).order_by('RollNo')
        if 'class' in request.data.keys():
            if request.data.get('class') is not None and request.data.get('class') !='':
                class_id = data['class']
                if class_id is not None and class_id !='' and class_id !='null':
                    studentclassLogobj = studentclassLogobj.filter(classid=class_id).order_by('RollNo')
                

        
        
        current_acedemic_obj=AcademicYear.objects.filter(Isdeleted=False,school_code=school_code,isActive=True).first()
        if current_acedemic_obj is not None:
            studentclassLogobj = studentclassLogobj.filter(AcademicyearId=current_acedemic_obj.id).order_by('RollNo')


        if studentclassLogobj.exists():
            studentclassser = custom_student_class_log_studentcode_list_serializer(studentclassLogobj,many=True)
            student_obj=Students.objects.filter(StudentCode__in=list(studentclassser.data),isActive=True).order_by('StudentCode').distinct('StudentCode')
            if student_obj.exists():
                if 'student_name' in request.data.keys():
                    if request.data.get('student_name') is not None and request.data.get('student_name') !='':
                        student_name = data['student_name']
                        if student_name is not None and student_name !='' and student_name !='null':
                            student_obj = student_obj.filter(StudentName__icontains=student_name)
                student_serializer_id=custom_student_serializer(student_obj,many=True)
                
                print("studentclassser",list(student_serializer_id.data))
                studentclassLogobj=studentclassLogobj.filter(studentId__in=list(student_serializer_id.data))
                class_serializer=custom_studentclassLogserializer(studentclassLogobj,many=True)
                return Response({"data":class_serializer.data,"response": {"n": 1, "msg": "Students found successfully","status": "success"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg": "No student found ","status": "failure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No student found ","status": "failure"}})
        
        
#Announcements-------------------------------------------------------------------------------------
class set_primary_student(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['school_code']=request.user.school_code
        data['ParentId']=str(request.user.id)
        parent_obj=User.objects.filter(id=data['ParentId'],isActive=True,school_code=data['school_code']).first()
        if parent_obj is not None:
            data['StudentCode']=str(data['StudentCode'])
            student_obj=Students.objects.filter(StudentCode=data['StudentCode'],ParentId=data['ParentId'],school_code=data['school_code']).first()
            if student_obj is not None:
                data['primary_student']=True
                Primary_Student_Serializer=StudentSerializer(student_obj,data=data,partial=True)
                if Primary_Student_Serializer.is_valid():
                    Primary_Student_Serializer.save()
                    return Response({"data":Primary_Student_Serializer.data,"response": {"n": 1, "msg": "Student set as a primary student ","status": "success"}})
                else:
                    first_key, first_value = next(iter(Primary_Student_Serializer.errors.items()))
                    return Response({"data":Primary_Student_Serializer.errors,"response": {"n": 0, "msg":str(first_key) +' : '+str(first_value[0]),"status": "failure"}})
            else:
                student_obj=Students.objects.filter(ParentId=data['ParentId'],school_code=data['school_code'])
                student_serializers=StudentSerializer(student_obj,many=True)
                
                return Response({"data":student_serializers.data,"response": {"n": 0, "msg":"student with this student code not found,available options are given below","status": "failure"}})
        return Response({"data":[],"response": {"n": 0, "msg":"parent with this parent id not found","status": "failure"}})
            
class add_announcement(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        data['isActive']=True
        serializer = AnnouncementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement added successfully',"status": "success"}})
        else:
            first_key, first_value = next(iter(serializer.errors.items()))
            return Response({"data":serializer.errors,"response": {"n": 0, "msg":first_key + " : "+ first_value[0],"status": "failure"}})
                            
class announcement_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        school_code=request.user.school_code
        obj=Announcements.objects.filter(isActive=True,school_code=school_code)
        serializer = CustomAnnouncementSerializer(obj,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcements found successfully',"status": "success"}})
                        
class edit_announcement(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        obj=Announcements.objects.filter(id=data['id'],isActive=True,school_code=data['school_code']).first()
        if obj is not None:
            serializer = AnnouncementSerializer(obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement updated successfully',"status": "success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":serializer.errors,"response": {"n": 0, "msg":first_key + " : "+ first_value[0],"status": "failed"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg":'announcement not found',"status": "failed"}})
                    
class get_announcement_details(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        obj=Announcements.objects.filter(id=data['id'],isActive=True,school_code=data['school_code']).first()
        if obj is not None:
            serializer = CustomAnnouncementSerializer2(obj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement found successfully',"status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg":'announcement not found',"status": "failed"}})

class delete_announcement(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        data['isActive']=False
        obj=Announcements.objects.filter(id=data['id'],isActive=True,school_code=data['school_code']).first()
        if obj is not None:
            serializer = AnnouncementSerializer(obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement deleted successfully',"status": "success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":serializer.errors,"response": {"n": 0, "msg":first_key + " : "+ first_value[0],"status": "failed"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg":'announcement not found',"status": "failed"}})
                              
class get_student_announcements(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        if data['StudentCode'] is None or data['StudentCode'] == "":
            return Response({"data":[],"response": {"n": 0, "msg":'Please provide StudentCode ',"status": "failed"}})
        student_obj=Students.objects.filter(StudentCode=data['StudentCode'],isActive=True,school_code=data['school_code']).first()
        if student_obj is not None:
            student_serializeer=StudentSerializer(student_obj)
            class_id=[str(student_serializeer.data['StudentClass'])]
            todays_date=str(datetime.today().date())
            print("todays_date",todays_date)
            obj=Announcements.objects.filter(classid__contains=class_id,isActive=True,school_code=data['school_code'],Date__gte=todays_date).order_by('Date')
            if obj.exists():
                serializer = CustomAnnouncementSerializer2(obj,many=True)
                return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement found successfully',"status": "success"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg":'Announcement not found',"status": "failed"}})

        else:
            return Response({"data":[],"response": {"n": 0, "msg":'student not found',"status": "failed"}})
class promote_students_class(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        data['promoted_class']=request.POST.get('promoted_class')
        data['promoted_academic_year_id']=request.POST.get('promoted_academic_year_id')

        if data['current_academic_year_id'] is not None and data['current_academic_year_id'] !='':
            if data['current_class'] is not None and data['current_class'] !='':
                if data['promoted_academic_year_id'] is not None and data['promoted_academic_year_id'] !='':
                    if data['promoted_class'] is not None and data['promoted_class'] !='':
                        data['students_ids_list']=json.loads(request.POST.get('students_ids_list'))
                        if data['students_ids_list'] is not None and data['students_ids_list'] !=[]:
                            get_studentlist=Students.objects.filter(id__in=data['students_ids_list'],isActive=True).order_by('StudentName')
                            students_serializer=StudentSerializer(get_studentlist,many=True)
                            promoted=[]
                            non_promoted=[]
                            counter=1
                            for student in students_serializer.data:
                                check_already_promoted_obj=studentclassLog.objects.filter(studentId=student['id'],AcademicyearId=data['promoted_academic_year_id'],school_code=data['school_code']).first()
                                if check_already_promoted_obj is not None:
                                    class_log_data={}
                                    class_log_data['classid']=data['promoted_class']
                                    class_log_data['promote_class']=False
                                    class_log_data['RollNo']=counter
                                    
                                    serializer=studentclassLogserializer(check_already_promoted_obj,data=class_log_data,partial=True)
                                    if serializer.is_valid():
                                        serializer.save()
                                        counter+=1

                                        Students.objects.filter(id=serializer.data['studentId'],isActive=True).update(StudentClass=serializer.data['classid'],RollNo=serializer.data['RollNo'])

                                        promoted.append(student['StudentName'])
                                    else:
                                        non_promoted.append(student['StudentName'])
                                        
                                else:
                                    check_previous_promoted_obj=studentclassLog.objects.filter(studentId=student['id'],AcademicyearId=data['current_academic_year_id'],school_code=data['school_code'],classid=data['current_class']).first()
                                    if check_previous_promoted_obj is not None:
                                        check_previous_promoted_obj.promote_class=True
                                        check_previous_promoted_obj.save()
                                    else:
                                        print("previous class not found for promotion")
                                    class_log_data={}
                                    class_log_data['AcademicyearId']=data['promoted_academic_year_id']
                                    class_log_data['studentId']=student['id']
                                    class_log_data['classid']=data['promoted_academic_year_id']
                                    class_log_data['school_code']=data['school_code']
                                    class_log_data['promote_class']=False
                                    class_log_data['StudentCode']=student['StudentCode']
                                    class_log_data['RollNo']=counter

                                    serializer=studentclassLogserializer(data=class_log_data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        counter+=1
                                        Students.objects.filter(id=serializer.data['studentId'],isActive=True).update(StudentClass=serializer.data['classid'],RollNo=serializer.data['RollNo'])

                                        promoted.append(student['StudentName'])
                                    else:
                                        non_promoted.append(student['StudentName'])

                            return Response({"data":{'promoted':promoted,'non_promoted':non_promoted},"response": {"n": 1, "msg":'Students promoted successfully',"status": "success"}})
                        else:
                            return Response({"data":{'promoted':[],'non_promoted':[]},"response": {"n": 0, "msg":'Please provide promoted student list',"status": "failed"}})
                    else:
                        return Response({"data":{'promoted':[],'non_promoted':[]},"response": {"n": 0, "msg":'Please provide promoted class',"status": "failed"}})
                else:
                    return Response({"data":{'promoted':[],'non_promoted':[]},"response": {"n": 0, "msg":'Please provide promoted academic year',"status": "failed"}})
            else:
                return Response({"data":{'promoted':[],'non_promoted':[]},"response": {"n": 0, "msg":'Please provide current class',"status": "failed"}})
        else:
            return Response({"data":{'promoted':[],'non_promoted':[]},"response": {"n": 0, "msg":'Please provide current academic year',"status": "failed"}})
        
class getPromotedList(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        
        schoolcode = request.user.school_code
        studentlist = []
                
        studentclassLogobj = studentclassLog.objects.filter(school_code=schoolcode)
        if 'class' in request.data.keys():
            if request.data.get('class') is not None and request.data.get('class') !='':
                class_id = data['class']
                studentclassLogobj = studentclassLogobj.filter(classid=class_id)
                
        if 'yearid' in request.data.keys():
            if request.data.get('yearid') is not None and request.data.get('yearid') !='':
                ac_yearid = data['yearid']
                studentclassLogobj = studentclassLogobj.filter(AcademicyearId=ac_yearid)
                
        if 'promote_classid' in request.data.keys():
            if request.data.get('promote_classid') is not None and request.data.get('promote_classid') !='':
                proid = data['promote_classid']
                studentclassLogobj = studentclassLogobj.filter(promote_class=proid)
        
        if studentclassLogobj.exists():
            studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
            for st in studentclassser.data:
                studeobj = Students.objects.filter(id=st['studentId']).first()
                st['StudentName'] = studeobj.StudentName

                classobj = Class.objects.filter(id=st['classid']).first()
                st['StudentClass'] = classobj.ClassName
                
            return Response({"data":studentclassser.data,"response": {"n": 1, "msg": "Data found successfully","status": "success"}})

class search_students(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        schoolcode = request.user.school_code
        studentlist = []
        studentclassLogobj = studentclassLog.objects.filter(school_code=schoolcode)
        if 'class' in request.data.keys():
            if request.data.get('class') is not None and request.data.get('class') !='':
                class_id = data['class']
                studentclassLogobj = studentclassLogobj.filter(classid=class_id)
                
        if 'yearid' in request.data.keys():
            if request.data.get('yearid') is not None and request.data.get('yearid') !='':
                ac_yearid = data['yearid']
                studentclassLogobj = studentclassLogobj.filter(AcademicyearId=ac_yearid)
                
        if studentclassLogobj.exists():
            studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
            for s in studentclassser.data:
                stuobj = Students.objects.filter(id=s['studentId'],StudentCode=s['StudentCode'],school_code=schoolcode,isActive=True).first()
                if stuobj is not None:
                    stuser = StudentSerializer1(stuobj) 
                    details = []
                    for t in [stuser.data]:
                        t['classid'] = s['classid']
                        details.append(t)
                    studentlist.append(details[0])
            return Response({"data":studentlist,"response": {"n": 1, "msg": "Students found successfully","status": "success"}})
                    
        else:

            return Response({"data":[],"response": {"n": 0, "msg": "No students found","status": "failure"}})

class GenerateMarksheetListApi(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        schoolcode = request.user.school_code
        
        stuobj = Students.objects.filter(school_code=schoolcode,isActive=True)
        stuser = StudentSerializer1(stuobj,many=True) 
        details = []
        for t in stuser.data:
            details.append(t)
   
class search_student(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        StudentName=data['StudentName']
        school_code = request.user.school_code
        student_obj=Students.objects.filter(StudentName__icontains=StudentName,isActive=True,school_code=school_code)
        if student_obj.exists():
            student_serializer=CustomStudentSerializer(student_obj,many=True)
            studentlist = student_serializer.data
            for student in studentlist:
                class_log_obj=studentclassLog.objects.filter(studentId=student['id'],school_code=school_code,isActive=True)
                class_log_serializer=custom_student_class_serializer(class_log_obj,many=True)
                student['class_log']=class_log_serializer.data
            return Response({"data":studentlist,"response": {"n": 1, "msg": "Data found successfully","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "No student found .","status": "failure"}})

class parent_bulk_upload(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        dataset = Dataset()
        fileerrorlist=[]
        new_parents = request.FILES['file']
        school_code = request.user.school_code
        if not new_parents.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})
        schoolobj = School.objects.filter(school_code = school_code,isActive=True).first()
        if schoolobj is not None:
            schoolname = schoolobj.Name
        else:
            schoolname = 'School ERP'
            
        imported_data = dataset.load(new_parents.read(), format='xlsx')
        for i in imported_data:
            
            parent_name=i[0]
            parent_email = i[1]
            parent_mobile_number = i[2]
            address = i[3]


            data={}          

            if parent_name is not None and parent_name !="":
                data['Username']=parent_name
                parent_name_exist = User.objects.filter(Username__in = [data['Username'].strip().capitalize(),data['Username'].strip(),data['Username'].title(),data['Username'].upper(),data['Username'].lower(),data['Username']],isActive= True,school_code=school_code).first()
                if parent_name_exist is not None:
                    reason = 'parent with this name is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'parent name is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  

            if parent_email is not None and parent_email !="":
                data['email']=parent_email
                parent_email_exist = User.objects.filter(email__in = [data['email'].strip().capitalize(),data['email'].strip(),data['email'].title(),data['email'].upper(),data['email'].lower(),data['email']],isActive= True,school_code=school_code).first()
                if parent_email_exist is not None:
                    reason = 'parent with this email is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'parent email is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
            if parent_mobile_number is not None and parent_mobile_number !="":
                data['mobileNumber']=str(parent_mobile_number)
                parent_mobile_number_exist = User.objects.filter(mobileNumber__in = [data['mobileNumber'].strip().capitalize(),data['mobileNumber'].strip(),data['mobileNumber'].title(),data['mobileNumber'].upper(),data['mobileNumber'].lower(),data['mobileNumber']],isActive= True,school_code=school_code).first()
                if parent_mobile_number_exist is not None:
                    reason = 'parent with this mobile number is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'parent mobile number is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
  
            if address is not None and address !="":
                data['Address']=address
                
            else:
                reason = 'parent address is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
            data['school_code']=school_code
            data['role']=5
            data['password'] = str(12345)
            data['textPassword'] = str(12345)
            
            

            
 
                
            serializer=UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                #send mail
                subject = "Registration succesful"
                data2 = {"Name": serializer.data['Username'],"email":serializer.data['email'],'userid':serializer.data['id'],'frontend_url':frontend_url,
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
 
                    data['n'] = 1
                    data['Msg'] = 'Email has been sent'
                    data['Status'] = "Success"
                    
                except Exception as e:
                    print("e",e)
                
                
                
                
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                reason = 'Error in adding Parent '+first_key +' : '+ first_value[0]
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
         
        if len(fileerrorlist) == 0:
            return Response({"data":'',"response": {"n": 1, "msg": "Parents excel uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['Parent Name','Parent email','Contact No','Address ','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})
    
class student_bulk_upload(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        dataset = Dataset()
        fileerrorlist=[]
        new_parents = request.FILES['file']
        school_code = request.user.school_code
        if not new_parents.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})

        Academic_obj=AcademicYear.objects.filter(school_code=school_code,isActive=True,Isdeleted=False).first()   
        
        imported_data = dataset.load(new_parents.read(), format='xlsx')
        for i in imported_data:
            parent_email=i[0]
            student_name = i[1]
            class_name = i[2]
            blood_group = i[3]
            date_of_birth = i[4]
            date_of_joining = i[5]
            student_roll_no = i[6]


            data={}          
            if Academic_obj is None:
                reason = 'Academic Year is not Active'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
            
            
            if parent_email is not None and parent_email !="":
                data['email']=parent_email
                parent_email_exist = User.objects.filter(email__in = [data['email'].strip().capitalize(),data['email'].strip(),data['email'].title(),data['email'].upper(),data['email'].lower(),data['email']],isActive= True,school_code=school_code).first()
                if parent_email_exist is not None:
                    data['ParentId']=str(parent_email_exist.id)
                else:
                    reason = 'parent with this email is not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'parent email is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
            
            
            if class_name is not None and class_name !="":
                class_name_exist = Class.objects.filter(ClassName__in = [class_name.strip().capitalize(),class_name.strip(),class_name.title(),class_name.upper(),class_name.lower(),class_name],isActive= True,school_code=school_code).first()
                if class_name_exist is not None:
                    data['StudentClass']=class_name_exist.id
                    
                else:
                    reason = 'Class with this name is not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'Class name is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
  
  
            if student_name is not None and student_name !="":
                data['StudentName']=student_name
                
            else:
                reason = 'student name is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  

  
            if blood_group is not None and blood_group !="":
                blood_group_exist = BloodGroup.objects.filter(Groupname__in = [blood_group.strip().capitalize(),blood_group.strip(),blood_group.title(),blood_group.upper(),blood_group.lower(),blood_group],isActive= True).first()
                if blood_group_exist is not None:
                    data['BloodGroup']=blood_group_exist.id
                    
                else:
                    reason = 'Blood Group with this name is not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'Blood Group  is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
  
            if date_of_birth is not None and date_of_birth !="":
                data['DateOfBirth']= str(date_of_birth).split(' ')[0]
            else:
                reason = 'Date Of Birth is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue 
            
            if date_of_joining is not None and date_of_joining !="":
                data['DateofJoining']= str(date_of_joining).split(' ')[0]
            else:
                reason = 'Date Of joining is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue 
            
            
            if student_roll_no is not None and student_roll_no !="":
                data['RollNo']= str(student_roll_no).split(' ')[0]
            else:
                reason = 'student roll no is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue 
  
            data['school_code']=school_code

            

            
            check_already_exist=Students.objects.filter(ParentId=data['ParentId'],StudentClass=data['StudentClass'],StudentName__in = [student_name.strip().capitalize(),student_name.strip(),student_name.title(),student_name.upper(),student_name.lower(),student_name],isActive= True,school_code=school_code).first()

            if check_already_exist is not None:
                serializer=StudentSerializer(check_already_exist,data=data,partial=True)
            else:
                data['StudentCode'] = createstudentid(school_code)
                serializer=StudentSerializer(data=data)
                

                
            if serializer.is_valid():
                serializer.save()
                class_data={}
                class_data['AcademicyearId']=Academic_obj.id
                class_data['studentId']=serializer.data['id']
                class_data['StudentCode']=serializer.data['StudentCode']
                class_data['classid']=serializer.data['StudentClass']
                class_data['school_code']=school_code
                
                check_already_exist_class_log_obj=studentclassLog.objects.filter(AcademicyearId=class_data['AcademicyearId'],studentId=class_data['studentId'],StudentCode=class_data['StudentCode'],classid=class_data['classid'],school_code=class_data['school_code']).first()
                if check_already_exist_class_log_obj is not None:
                    class_log_serializer=studentclassLogserializer(check_already_exist_class_log_obj,data=class_data,partial=True)
                else:
                    class_log_serializer=studentclassLogserializer(data=class_data)
                    
                if class_log_serializer.is_valid():
                    class_log_serializer.save()
                else:
                    first_key, first_value = next(iter(class_log_serializer.errors.items()))
                    reason = 'Error in adding student class'+first_key +' : '+ first_value[0]
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue
                # create student class log
                
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                reason = 'Error in adding student '+first_key +' : '+ first_value[0]
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
         
        if len(fileerrorlist) == 0:
            return Response({"data":'',"response": {"n": 1, "msg": "Students excel uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['Parent Name','Parent email','Contact No','Address ','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})
   
