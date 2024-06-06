from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from DesignationMaster.models import Designation
from DesignationMaster.serializers import DesignationSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from User.jwt import userJWTAuthentication



class AddDesignation(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        data['school_code']=request.user.school_code
        Desgnexist = Designation.objects.filter(designationName=data['designationName'],isActive= True,school_code=data['school_code']).first()
        if Desgnexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "Designation already exist","status": "failure"}})
        else:
            serializer = DesignationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Designation added successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Designation not added ","status": "failure"}})

        
class Designationlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        school_code=request.user.school_code
        desgobjs = Designation.objects.filter(isActive=True,school_code=school_code).order_by('-id')
        serializer = DesignationSerializer(desgobjs,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "Designation list found successfully","status": "success"}})
      
       
class getDesignationbyid(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        id = request.data.get('id')
        desgobj = Designation.objects.filter(id=id,isActive=True).first()
        if desgobj is not None:
            serializer = DesignationSerializer(desgobj)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Designation found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Designation not found ","status": "failure"}})



class updatedesignation(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        desgid = data['id']
        desgobj = Designation.objects.filter(id=desgid,isActive=True).first()
        if desgobj is not None:
            desgexist = Designation.objects.filter(designationName=data['designationName'],isActive= True).exclude(id=desgid).first()
            if desgexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "Designation already exist","status": "failure"}})
            else:
                serializer = DesignationSerializer(desgobj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "Designation Updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Update Designation ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Designation not found ","status": "failure"}})

class deletedesignation(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        desgid = data['id']
        desgobj = Designation.objects.filter(id=desgid,isActive=True).first()
        if desgobj is not None:
            data['isActive'] = False
            serializer = DesignationSerializer(desgobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Designation Deleted successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Delete Designation ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Designation not found ","status": "failure"}})