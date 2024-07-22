

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
from SubjectMaster.serializers import SubjectSerializer
from User.models import User
from DesignationMaster.models import Designation
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
from Frontend.school.static_info import frontend_url
from tablib import Dataset

class AddTeacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        subjects = json.loads(data['subjects'])
        schoolcode = request.user.school_code
        teacherexist = User.objects.filter(Username=data['Name'],isActive= True,school_code=schoolcode).first()
        if teacherexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher Name already exist","status": "failure"}})
        
        teacheremailexist = User.objects.filter(email=data['Email'],isActive= True,school_code=schoolcode).first()
        if teacheremailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
        
        teachermobileexist = User.objects.filter(mobileNumber=data['MobileNumber'],isActive= True,school_code=schoolcode).first()
        if teachermobileexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Mobile Number already exist","status": "failure"}})
        
        else:
            teachercreate = User.objects.create(email=data['Email'],Username = data['Name'], school_code = schoolcode,role_id = 4,password = str(12345),textPassword = str(12345),designation_id=data['Designation'],mobileNumber=data['MobileNumber'],joiningDate=data['joiningDate'],Address=data['Address'])

            teacherobj = User.objects.filter(email=data['Email'],isActive=True,school_code=schoolcode).first()
            if teacherobj is not None :
                teacherid = teacherobj.id

                for s in subjects:
                    TeacherSubject.objects.create(TeacherId=str(teacherid),SubjectId_id=s,school_code=schoolcode)



                #send mail
                subject = "Registration successful"
                data2 = {"Name": data['Name'],"email":data['Email'],'userid':teacherid,'frontend_url':frontend_url,
                            "template": 'mails/teacher_registration.html'}
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
        teacherobj = User.objects.filter(isActive=True,role_id=4,school_code = schoolcode).order_by('-createdAt')
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
        school_code = request.user.school_code
        teacher_obj = User.objects.filter(id=data['id'],isActive= True).first()
        if teacher_obj is not None:
            
            teacherexist = User.objects.filter(Username=data['Username'],isActive= True,school_code=school_code).exclude(id=data['id']).first()
            if teacherexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Teacher Name already exist","status": "failure"}})
            
            teacheremailexist = User.objects.filter(email=data['email'],isActive= True,school_code=school_code).exclude(id=data['id']).first()
            if teacheremailexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Email already exist","status": "failure"}})
            
            teachermobileexist = User.objects.filter(mobileNumber=data['mobileNumber'],isActive= True).exclude(id=data['id'],school_code=school_code).first()
            if teachermobileexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Mobile Number already exist","status": "failure"}})
            
            else:
                serializer=UserSerializer(teacher_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    delete_subject=TeacherSubject.objects.filter(TeacherId=str(serializer.data['id'])).delete()
                    for s in subjects:
                        subject_obj=TeacherSubject.objects.create(TeacherId=str(serializer.data['id']),SubjectId_id=s,school_code=school_code)
                            
                    return Response({"data":'',"response": {"n": 1, "msg": "Teacher updated successfully","status": "success"}})
                else:
                    first_key, first_value = next(iter(serializer.errors.items()))
                    return Response({"data":'',"response": {"n": 0, "msg": first_key +' ' +first_value[0],"status": "failure"}})

        else:
            
            return Response({"data":'',"response": {"n": 0, "msg": "Teacher not found","status": "failure"}})



class teacherdatabyexcel(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        school_code = request.user.school_code
        dataset = Dataset()
      
        new_product = request.FILES.get('classfile')

        if not new_product.name.endswith('xlsx'):
            return Response({"data":'',"response": {"n": 0, "msg": "Wrong File Format","status": "failure"}})

        imported_data = dataset.load(new_product.read(), format='xlsx')
        
        importDataList =[]
        notimporteddatalist = []
        for i in imported_data:
            if i[0] is not None:
                importDataList.append(i)
            else:
                notimporteddatalist.append(i)

        for i in importDataList:
            teacherexist = TeacherSubject.objects.filter(TeacherId__in=[i[0]],SubjectId_id__in=[i[0]],school_code=school_code).first()
            if teacherexist is None:
                TeacherSubject.objects.create(TeacherId=i[0],SubjectId_id=i[0],school_code=school_code)
                
        return Response({"data":'done',"response": {"n": 1, "msg": "Teacher master uploaded successfully","status": "success"}})


class UploadTeachersExcel(GenericAPIView): 
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        dataset = Dataset()
        fileerrorlist=[]
        new_teachers = request.FILES['file']
        school_code = request.user.school_code
        if not new_teachers.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})
        
        imported_data = dataset.load(new_teachers.read(), format='xlsx')
        for i in imported_data:
            teacher_name=i[0]
            teacher_email = i[1]
            teacher_designation = i[2]
            joining_date = i[3]
            teacher_mobile_number = i[4]
            subjects = i[5]
            address = i[6]
            data={}

            
            if teacher_name is not None and teacher_name !="":
                data['Username']=teacher_name
                
                
                teacher_name_exist = User.objects.filter(Username__in = [data['Username'].strip().capitalize(),data['Username'].strip(),data['Username'].title(),data['Username'].upper(),data['Username'].lower(),data['Username']],isActive= True,school_code=school_code).first()
                if teacher_name_exist is not None:
                    reason = 'teacher with this name is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'teacher name is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  

            if teacher_email is not None and teacher_email !="":
                data['email']=teacher_email
                
                teacher_email_exist = User.objects.filter(email__in = [data['email'].strip().capitalize(),data['email'].strip(),data['email'].title(),data['email'].upper(),data['email'].lower(),data['email']],isActive= True,school_code=school_code).first()
                if teacher_email_exist is not None:
                    reason = 'teacher with this email is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'teacher email is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
  
            if teacher_designation is not None and teacher_designation !="":
                data['designation']=teacher_designation
                teacher_designation_exist = Designation.objects.filter(designationName__in = [data['designation'].strip().capitalize(),data['designation'].strip(),data['designation'].title(),data['designation'].upper(),data['designation'].lower(),data['designation']],isActive= True,school_code=school_code).first()
                if teacher_designation_exist is not None:
                    data['designation']=teacher_designation_exist.id
                else:
                    reason = ' designation not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'teacher designation is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
                
            if joining_date is not None and joining_date !="":
                data['joiningDate'] = str(joining_date).split(' ')[0]
            else:
                reason = 'teacher joining date is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  
            
            if teacher_mobile_number is not None and teacher_mobile_number !="":
                data['mobileNumber']=teacher_mobile_number
                
                teacher_mobile_number_exist = User.objects.filter(mobileNumber=data['mobileNumber'],isActive= True,school_code=school_code).first()
                if teacher_mobile_number_exist is not None:
                    reason = 'teacher with this mobile number is already exists.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue  
            else:
                reason = 'teacher mobile number is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue  

  
            data['subject_ids']=[]
            if subjects is not None and subjects !="":
                data['subjects'] = str(subjects).split(",")
                if len(data['subjects']) !=[]:
                    for sub in data['subjects']:
                        subject_obj=Subject.objects.filter(SubjectName__in = [sub.strip().capitalize(),sub.strip(),sub.title(),sub.upper(),sub.lower(),sub],isActive= True,school_code=school_code).first()
                        if subject_obj is not None:
                            data['subject_ids'].append(subject_obj.id)
            
                else:
                    reason = 'Valid teacher subjects is required.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'teacher subjects is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue 
            
            if address is not None and address !="":
                data['Address'] = str(address)
            else:
                reason = 'teacher address is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue 
            
            
            data['school_code']=school_code
            data['role']=4
            data['password']=str(12345)
            data['textPassword']=str(12345)
            serializer=UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                teacherid = serializer.data['id']
                for s in data['subject_ids']:
                    TeacherSubject.objects.create(TeacherId=str(teacherid),SubjectId_id=s,school_code=school_code)

                subject = "Registration successful"
                data2 = {"Name": serializer.data['Username'],"email":serializer.data['email'],'userid':teacherid,'frontend_url':frontend_url,
                            "template": 'mails/teacher_registration.html'}
                message = render_to_string(
                        data2['template'], data2)
                try:
                    msg = EmailMessage(
                        subject,
                        message,
                        EMAIL_HOST_USER,
                        [serializer.data['email']],
                    )
                    msg.content_subtype = "html"
                    m = msg.send()
                    
          
                    
                except Exception as e:
                    print("exception raised",e)
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                reason = 'Error in adding teacher '+first_key +' : '+ first_value[0]
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
         
        if len(fileerrorlist) == 0:
            return Response({"data":'',"response": {"n": 1, "msg": "Teacher excel uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['Teacher Name','Teacher Email ','Designation','Joining Date ','Contact No ','Subject ','Address','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})
    
