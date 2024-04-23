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