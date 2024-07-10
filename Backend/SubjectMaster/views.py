from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
from SubjectMaster.serializers import SubjectSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from User.jwt import userJWTAuthentication
from tablib import Dataset



class AddSubject(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        school_code = request.user.school_code
        data['school_code']=school_code
        subjectnexist = Subject.objects.filter(SubjectName=data['SubjectName'],isActive= True,school_code=school_code).first()
        if subjectnexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Subject already exist","status": "failure"}})
        else:
            serializer = SubjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Subject added successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Subject not added ","status": "failure"}})

        
class Subjectlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        school_code = request.user.school_code
        subjectobjs = Subject.objects.filter(isActive=True,school_code=school_code).order_by('SubjectName')
        serializer = SubjectSerializer(subjectobjs,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "Subject list found successfully","status": "success"}})
      
       
class getSubjectbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id = request.data.get('id')
        subjectobj = Subject.objects.filter(id=id,isActive=True).first()
        if subjectobj is not None:
            serializer = SubjectSerializer(subjectobj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Subject found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Subject not found ","status": "failure"}})



class updateSubject(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        subjectid = data['id']
        subjectobj = Subject.objects.filter(id=subjectid,isActive=True).first()
        if subjectobj is not None:
            subjectexist = Subject.objects.filter(SubjectName=data['SubjectName'],isActive= True).exclude(id=subjectid).first()
            if subjectexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Subject already exist","status": "failure"}})
            else:
                serializer = SubjectSerializer(subjectobj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Subject Updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Update Subject ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Subject not found ","status": "failure"}})

class deleteSubject(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        subjectid = data['id']
        subjectobj = Subject.objects.filter(id=subjectid,isActive=True).first()
        if subjectobj is not None:
            data['isActive'] = False
            serializer = SubjectSerializer(subjectobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Subject Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Subject ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Subject not found ","status": "failure"}})





class subjectdatabyexcel(GenericAPIView):
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
            SubjectName =i[0]
            data={}
            
            if SubjectName is not None and SubjectName !="":
                data['SubjectName']= SubjectName
                SubjectName_exist = Subject.objects.filter(SubjectName__in = [data['SubjectName'].strip().capitalize(),data['SubjectName'].strip(),data['SubjectName'].title(),data['SubjectName'].upper(),data['SubjectName'].lower(),data['SubjectName']],isActive= True,school_code=school_code).first()
                if SubjectName_exist is None:
                    Subject.objects.create(SubjectName= data['SubjectName'],school_code=school_code)
                else:
                    reason = 'Subject already exits.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue 
            else:
                reason = 'Subject master is required.'
                error = i + tuple([reason])
                fileerrorlist.append(error)
                continue
  

        if len(fileerrorlist) == 0:
            return Response({"data":'done',"response": {"n": 1, "msg": "Subject master uploaded successfully","status": "success"}})
        else:
            return Response({"data":fileerrorlist,'headers':['SubjectName','Failure Reason'],"response": {"n": 2, "msg": "file has some issues","status": "failure"}})



