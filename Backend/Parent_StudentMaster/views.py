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
        print("data",data)
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
                        # print()
                        if stuobj is not None :
                            # if s['photo'] != "" and s['photo'] is not None:
                            #     s['photo'] = s['photo']
                            # else:
                            #     s['photo'] = stuobj.photo
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
                                    class_lof_obj=studentclassLog.objects.filter(studentId=class_data['studentId'],StudentCode=class_data['StudentCode']).first()
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
        

# class getstudentlist(GenericAPIView):
#     authentication_classes=[userJWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self,request):
#         data = request.data.copy()
#         class_id = data['class']
#         ac_yearid = data['yearid']
        
#         schoolcode = request.user.school_code
#         studentlist = []

#         studentclassLogobj = studentclassLog.objects.filter(AcademicyearId=ac_yearid,classid=class_id,school_code=schoolcode)
#         if studentclassLogobj.exists():
#             studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
#             for s in studentclassser.data:
#                 stuobj = Students.objects.filter(id=s['studentId'],StudentCode=s['StudentCode'],school_code=schoolcode,isActive=True).first()
#                 if stuobj is not None:
#                     stuser = StudentSerializer(stuobj) 
#                     studentlist.append(stuser.data)
                    
#         return Response({"data":studentlist,"response": {"n": 1, "msg": "student list found ","status": "success"}})
       

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
            
        if studentclassLogobj.exists():
            studentclassser = studentclassLogserializer(studentclassLogobj,many=True)
            for s in studentclassser.data:
                stuobj = Students.objects.filter(id=s['studentId'],StudentCode=s['StudentCode'],school_code=schoolcode,isActive=True).first()
                if stuobj is not None:
                    stuser = StudentSerializer1(stuobj) 
                    studentlist.append(stuser.data)
        # else:
        #     stuobj = Students.objects.filter(school_code=schoolcode,isActive=True)
        #     stuser = StudentSerializer1(stuobj,many=True) 
        #     studentlist=stuser.data
        
        
        
        return Response({"data":studentlist,"response": {"n": 1, "msg": "student list found ","status": "success"}})




class getstudentidcards(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        idcardlist = []
        data = request.data.copy()
        print("data",data)
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
        print("dta",data)
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
        
        student_obj=Students.objects.filter(StudentCode=data['StudentCode'],isActive=True,school_code=data['school_code']).first()
        if student_obj is not None:
            student_serializeer=StudentSerializer(student_obj)
            class_id=[str(student_serializeer.data['StudentClass'])]
            obj=Announcements.objects.filter(classid__contains=class_id,isActive=True,school_code=data['school_code']).order_by('-Date')
            if obj.exists():
                serializer = CustomAnnouncementSerializer2(obj,many=True)
                return Response({"data":serializer.data,"response": {"n": 1, "msg":'Announcement found successfully',"status": "success"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg":'Announcement not found',"status": "failed"}})

        else:
            return Response({"data":[],"response": {"n": 0, "msg":'student not found',"status": "failed"}})




