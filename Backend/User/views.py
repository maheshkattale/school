from django.shortcuts import render

# Create your views here.from rest_framework.response import Response
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from rest_framework import permissions
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .jwt import userJWTAuthentication
from django.contrib.auth.hashers import make_password,check_password


def createtoken(uuid,email,source):
    token = jwt.encode(
        {'id': uuid,
            'email': email,
            'source':source
           },
        settings.SECRET_KEY, algorithm='HS256')
    return token



class login(GenericAPIView):
    def post(self,request):
        email = request.data.get("email")
        Password = request.data.get("password")
        print("email",email,"ppp",Password,type(Password))
        source = request.data.get("source")
        if email is None or Password is None :
            return Response({'msg': 'Please provide username and password','n':0})
        
        userexist = User.objects.filter(email=email, isActive=True).first()
        if userexist is None:
           return Response({'msg': 'This user is not active','n':0})
        else:
            print("userexist",userexist.email , "pass",userexist.password )
            # user = authenticate(email=email,password=password)
            p = check_password(Password,userexist.password)
            print("P",p)
            if p is False:
                return Response({'msg': 'Invalid Credentials','n':0})
            else:
                useruuid = str(userexist.id)
                role = userexist.role
                username = userexist.Username
                schoolcode = userexist.school_code
                Token = createtoken(useruuid,email,source)
                print("TTTToken",Token)
                if source == "Web":
                    web_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createwebtoken = UserToken.objects.create(User=useruuid,WebToken=Token,source=source)
                elif source == "Mobile":
                    mobile_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createmobiletoken = UserToken.objects.create(User=useruuid,MobileToken=Token,source=source)
                else:
                    return Response({'msg': 'Please Provide Source','n':0})
                
                return Response({
                    "data" : {'token':Token,'username':username,'schoolcode':schoolcode},
                    "response":{
                    "n": 1 ,
                    "msg" : "login successful",
                    "status":"success"
                    }
                })
            


class logout(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
      
        auth_header = get_authorization_header(request)
        # print("ss",auth_header)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        token = auth_token[1]
        mobiletoken = UserToken.objects.filter(MobileToken=token,isActive=True).update(isActive=False)
        webtoken = UserToken.objects.filter(WebToken=token,isActive=True).update(isActive=False)
        return Response({
                        "data" : '',
                        "response":{
                        "n": 1 ,
                        "msg" : "logout successful",
                        "status":"success"
                        }
                    })



class Userlist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        userobj = User.objects.filter(isActive=True)
        userserializer = UserSerializer(userobj,many=True)
        return Response({"data":userserializer.data,"response": {"n": 1, "msg": "users found successfully","status": "success"}})
    

class Menulist(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(request):
        schoolcode = request.user.school_code
        menu_list = MenuItem.objects.filter(school_code=schoolcode)
        serializer = MenuItemSerializer(menu_list,many=True)
        return Response({
                "data" : serializer.data ,
                "response":{
                "n": 1 ,
                "msg" : "SUCCESS",
                "status":"success"
                }
                
            })
    

class getpermissions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(request):
        roleid = request.data.get('roleid')
        schoolcode = request.user.school_code
        psdata = permission.objects.filter(Role_id=roleid,school_code=schoolcode)
        serializer = permissionserializer(psdata,many=True)
        return Response({
            "data" : serializer.data,
            "response":{
                "n":1,
                "msg":"Permissions found Successfully",
                "status":"success"
                }
        })
    

    
class savepermissions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(request):
        roleid = request.data['roleid']
        permissionlist = request.data.getlist('permission')
        schoolcode = request.user.school_code
        permissiondata = permission.objects.filter(Role_id=roleid).first()
        data = {}
        data['Role_id'] = roleid
        data['permission'] = permissionlist
        data['school_code'] = schoolcode
        if permissiondata is not None:
            serializer = permissionserializer (permissiondata,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "data" : serializer.data ,
                    "response":{
                        "n": 1,
                        "msg" : "Permission Added Successfully",
                        "status":"success"
                        }
                })
            else:
                return Response({
                    "data" : serializer.errors ,
                    "response":{
                        "n": 1,
                        "msg" : "Permission not added",
                        "status":"failed"
                        }
                })

        else:
            serializer = permissionserializer (data=data)
            if serializer.is_valid():
                serializer.save() 
                return Response({
                    "data" : serializer.data ,
                    "response":{
                        "n": 1,
                        "msg" :  "Permission Added Successfully",
                        "status":"success"
                        }
                })
            return Response({
                    "data" : serializer.errors ,
                    "response":{
                        "n": 1,
                        "msg" : "Permission not added",
                        "status":"success"
                        }
                })



