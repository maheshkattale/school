from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from User.jwt import userJWTAuthentication
# from tablib import Dataset
from tablib import Dataset




class AddClass(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        schoolcode = request.user.school_code
        data['school_code'] = schoolcode
        classexist = Class.objects.filter(ClassName=data['ClassName'],isActive= True,school_code=schoolcode).first()
        if classexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Class already exist","status": "failure"}})
        else:
            serializer = ClassSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class added successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Class not added ","status": "failure"}})

        
class classlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        classobjs = Class.objects.filter(isActive=True,school_code=schoolcode).order_by('-id')
        serializer = ClassSerializer(classobjs,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class list found successfully","status": "success"}})
      
       
class getclassbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id = request.data.get('id')
        schoolcode = request.user.school_code
        classobj = Class.objects.filter(id=id,isActive=True,school_code=schoolcode).first()
        if classobj is not None:
            serializer = ClassSerializer(classobj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Class not found ","status": "failure"}})



class updateclass(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        classid = data['id']
        schoolcode = request.user.school_code
        classobj = Class.objects.filter(id=classid,isActive=True,school_code=schoolcode).first()
        if classobj is not None:
            classexist = Class.objects.filter(ClassName=data['ClassName'],isActive= True,school_code=schoolcode).exclude(id=classid).first()
            if classexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Class already exist","status": "failure"}})
            else:
                serializer = ClassSerializer(classobj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class Updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Update Class ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Class not found ","status": "failure"}})



class deleteclass(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        classid = data['id']
        schoolcode = request.user.school_code
        classobj = Class.objects.filter(id=classid,isActive=True,school_code=schoolcode).first()
        if classobj is not None:
            data['isActive'] = False
            serializer = ClassSerializer(classobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Class ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Class not found ","status": "failure"}})
        

class classdatabyexcel(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        school_code = request.user.school_code
        dataset = Dataset()
        fileerrorlist=[]
        new_product = request.FILES.get('classfile')

        if not new_product.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})

        imported_data = dataset.load(new_product.read(), format='xlsx')
        for i in imported_data:
            ClassName =i[0]
            data={}
            
            if ClassName is not None and ClassName !="":
                data['ClassName']= ClassName
                ClassName_exist = Class.objects.filter(ClassName__in = [data['ClassName'].strip().capitalize(),data['ClassName'].strip(),data['ClassName'].title(),data['ClassName'].upper(),data['ClassName'].lower(),data['ClassName']],isActive= True,school_code=school_code).first()
                if ClassName_exist is None:
                    Class.objects.create(ClassName= data['ClassName'],school_code=school_code)
                else:
                    reason = 'Class name already exits.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'Class name is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
  
        if len(fileerrorlist) == 0:
            return Response({"data":'done',"response": {"n": 1, "msg": "Class Name uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['ClassName','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})



class add_class_teacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        schoolcode = request.user.school_code
        data['school_code'] = schoolcode
        class_teacher_exist = ClassTeacher.objects.filter(classid=data['classid'],teacherid=data['teacherid'],academic_year_id=data['academic_year_id'],isActive= True,school_code=schoolcode).first()
        if class_teacher_exist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Class teacher already exist","status": "failure"}})
        else:
            serializer = ClassTeacherSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class teacher assigned successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "unable to assign class teacher ","status": "failure"}})

       

class get_class_teachers(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        class_teacher_exist = ClassTeacher.objects.filter(isActive= True,school_code=schoolcode)
        if class_teacher_exist.exists():
            serializer = CustomClassTeacherSerializer(class_teacher_exist,many=True)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class teachers founds successfully","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "class teacher not found","status": "failure"}})

class delete_class_teacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        class_teacher = data['id']
        schoolcode = request.user.school_code
        class_teacher_obj = ClassTeacher.objects.filter(id=class_teacher,isActive=True,school_code=schoolcode).first()
        if class_teacher_obj is not None:
            data['isActive'] = False
            serializer = ClassTeacherSerializer(class_teacher_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class Teacher Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Class Teacher! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Class teacher not found ","status": "failure"}})
        



class edit_class_teacher(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        schoolcode = request.user.school_code
        data['school_code'] = schoolcode
        class_teacher_obj = ClassTeacher.objects.filter(id=data['id'],isActive= True,school_code=schoolcode).first()
        if class_teacher_obj is not None:
            class_teacher_exist = ClassTeacher.objects.filter(classid=data['classid'],teacherid=data['teacherid'],academic_year_id=data['academic_year_id'],isActive= True,school_code=schoolcode).exclude(id=data['id']).first()
            if class_teacher_exist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Class teacher already exist","status": "failure"}})
            else:
                serializer = ClassTeacherSerializer(class_teacher_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Class teacher updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "unable to update class teacher ","status": "failure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": " class teacher not found ","status": "failure"}})
       


class teacher_classes_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        schoolcode = request.user.school_code
        teacherid=request.user.id
        current_academic_year=AcademicYear.objects.filter(Isdeleted=False,isActive=True,school_code=schoolcode).first()
        if current_academic_year is not None:
            teacher_classes_objs = ClassTeacher.objects.filter(teacherid=teacherid,isActive= True,school_code=schoolcode)
            if teacher_classes_objs.exists():
                serializer = CustomClassTeacherSerializer(teacher_classes_objs,many=True)
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "teacher Classes founds successfully","status": "success"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg": " teacher class not found","status": "failure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "current academic year is not set","status": "failure"}})



class classteacherdatabyexcel(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        school_code = request.user.school_code
        dataset = Dataset()
        fileerrorlist=[]
        new_product = request.FILES.get('classfile')

        if not new_product.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})

        imported_data = dataset.load(new_product.read(), format='xlsx')
        for i in imported_data:
            classid =i[0]
            teacherid =i[1]
            academic_year_id =i[2]
            data={}
            
            if classid is not None and classid !="":
                ClassName_exist = Class.objects.filter(ClassName__in = [i[0].strip().capitalize(),i[0].strip(),i[0].title(),i[0].upper(),i[0].lower(),i[0]],isActive= True,school_code=school_code).first()
                if ClassName_exist is not None:
                    data['classid']= ClassName_exist.id
                else:
                    reason = 'Class name not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
                
                teacher = User.objects.filter(Username__in = [i[1].strip().capitalize(),i[1].strip(),i[1].title(),i[1].upper(),i[1].lower(),i[1]],isActive= True,school_code=school_code).first()
                if teacher is not None:
                    data['teacherid']= teacher.id
                else:
                    reason = 'Tecaher name not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
                
                ExamType_exist = AcademicYear.objects.filter(startdate__in=[i[2].split('to')[0].strip()],enddate__in=[i[2].split('to')[1].strip()],school_code=school_code).first()
                if ExamType_exist is not None:
                    data['academic_year_id']= ExamType_exist.id
                else:
                    reason = 'Academic Year not found.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
                
                Classteacher_exist = ClassTeacher.objects.filter(classid__in=[data['classid']],teacherid__in=[data['teacherid']],academic_year_id__in=[data['academic_year_id']],isActive= True,school_code=school_code).first()
                if Classteacher_exist is None:
                    ClassTeacher.objects.create(classid_id=int(data['classid']),teacherid_id=int(data['teacherid']),academic_year_id_id=int(data['academic_year_id']),school_code=school_code)
                    
                else:
                    reason = 'Class teacher already exit.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'Class teacher is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
                
        if len(fileerrorlist) == 0:
            return Response({"data":'done',"response": {"n": 1, "msg": "Class Name uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['Class','ClassTeacherName','AcademicYear','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})










