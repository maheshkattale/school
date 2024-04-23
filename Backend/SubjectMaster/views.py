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



class AddSubject(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        subjectnexist = Subject.objects.filter(SubjectName=data['SubjectName'],isActive= True).first()
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
        subjectobjs = Subject.objects.filter(isActive=True).order_by('-id')
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
