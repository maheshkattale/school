from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from MarksheetMaster.models import *
from MarksheetMaster.serializers import *
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from User.jwt import userJWTAuthentication



class AddExamType(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        examtypeexist = ExamType.objects.filter(TypeName=data['TypeName'],Marks=data['Marks'],isActive= True).first()
        if examtypeexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "TypeName with marks already exist","status": "failure"}})
        else:
            serializer = ExamTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "ExamType added successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "ExamType not added ","status": "failure"}})

        
class ExamTypelist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        ExamTypeobjs = ExamType.objects.filter(isActive=True).order_by('-id')
        serializer = ExamTypeSerializer(ExamTypeobjs,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "ExamType list found successfully","status": "success"}})
      
       
class ExamTypebyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id = request.data.get('id')
        ExamTypeobj = ExamType.objects.filter(id=id,isActive=True).first()
        if ExamTypeobj is not None:
            serializer = ExamTypeSerializer(ExamTypeobj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "ExamType found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "ExamType not found ","status": "failure"}})



class updateExamType(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        ExamTypeid = data['id']
        ExamTypeobj = ExamType.objects.filter(id=ExamTypeid,isActive=True).first()
        if ExamTypeobj is not None:
            ExamTypeexist = ExamType.objects.filter(TypeName=data['TypeName'],Marks=data['Marks'],isActive= True).exclude(id=ExamTypeid).first()
            if ExamTypeexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "ExamType already exist","status": "failure"}})
            else:
                serializer = ExamTypeSerializer(ExamTypeobj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "ExamType Updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Update ExamType ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "ExamType not found ","status": "failure"}})


class deleteExamType(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        ExamTypeid = data['id']
        ExamTypeobj = ExamType.objects.filter(id=ExamTypeid,isActive=True).first()
        if ExamTypeobj is not None:
            data['isActive'] = False
            serializer = ExamTypeSerializer(ExamTypeobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "ExamType Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete ExamType ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "ExamType not found ","status": "failure"}})


# class AddExam(GenericAPIView):
#     authentication_classes=[userJWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self,request):
#         data = request.data.copy()
#         classlist = json.loads(data['classlist'])
