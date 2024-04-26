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
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from SchoolErp.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password,check_password
frontend_url = 'http://127.0.0.1:8000/'

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
        source = request.data.get("source")
        if email is None or Password is None :
            return Response(
                                                {
                    "data" : {'token':'','username':'','user_id':'','schoolcode':''},
                    "response":{
                    "status":"error",
                    'msg': 'Please provide username and password',
                    'n':0
                    }})
        
        userexist = User.objects.filter(email=email, isActive=True).first()
        if userexist is None:
           return Response(
                    {
                    "data" : {'token':'','username':'','user_id':'','schoolcode':''},
                    "response":{
                    "status":"error",
                    'msg': 'This user is not active',
                    'n':0
                    }}
                           )
        else:
            # user = authenticate(email=email,password=password)
            p = check_password(Password,userexist.password)
            if p is False:
                return Response(
                                
                    {
                    "data" : {'token':'','username':'','user_id':'','schoolcode':''},
                    "response":{
                    "status":"error",
                    'msg': 'Invalid Credentials',
                    'n':0
                    }}
                                
                                )
            else:
                useruuid = str(userexist.id)
                role = userexist.role
                username = userexist.Username
                schoolcode = userexist.school_code
                Token = createtoken(useruuid,email,source)
                if source == "Web":
                    web_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createwebtoken = UserToken.objects.create(User=useruuid,WebToken=Token,source=source)
                elif source == "Mobile":
                    mobile_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createmobiletoken = UserToken.objects.create(User=useruuid,MobileToken=Token,source=source)
                else:
                    return Response({
                    "data" : {'token':'','username':'','user_id':'','schoolcode':''},
                    "response":{
                    "status":"error",
                    'msg': 'Please Provide Source',
                    'n':0
                    }
                })
                
                return Response({
                    "data" : {'token':Token,'username':username,'user_id':useruuid,'schoolcode':schoolcode},
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
    def get(self,request):
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
    def get(self,request):
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
    

class getrole(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        role_objs = Role.objects.all()
        serializer = Roleserializer(role_objs,many=True)
        return Response({
            "data" : serializer.data,
            "response":{
                "n":1,
                "msg":"Roles found Successfully",
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


class ChangePassword(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = {}
        id = request.user.id
        if id is not None:
            userObject = User.objects.filter(id=id,isActive=True).first()
        
            if userObject:
                password = request.POST.get('oldpassword')
                currentPassword = check_password(password,userObject.password)
            
                if currentPassword==True:
                    newpassword = request.POST.get('newpassword')
                
                    confirmpassword = request.POST.get('confirmpassword')
                
                    if newpassword==confirmpassword:
                        data['password']= make_password(newpassword)
                        data['textPassword'] = newpassword
                        userSerializer = UserSerializer(userObject,data=data,partial=True)
                        if userSerializer.is_valid():
                            userSerializer.save()

                            tokenfalse = UserToken.objects.filter(User=id,isActive=True).update(isActive=False)
                           
                            return Response({"data":'',"response": {"n": 1, "msg": "password updated successfully","status": "success"}})
                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": "password not updated ","status": "failed"}})
                    else:
                        return Response({"data":'',"response": {"n": 0, "msg": "new and confirm password not matched ","status": "failed"}})
                else:
                    return Response({"data":'',"response": {"n": 0, "msg": "old password is wrong","status": "failed"}})

        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Couldnt find id","status": "failed"}})



class forgetpasswordmail(GenericAPIView):
    def post(self,request):
        data={}
        data['Email']=request.data.get('Email')
        userdata = User.objects.filter(email=data['Email'],isActive=True,PasswordSet=True).first()
        if userdata is not None:
            email =   data['Email']
            data2 = {'user_id':userdata.id,'user_email':userdata.email,'frontend_url':frontend_url}
            html_mail = render_to_string('mails/reset_password.html',data2)
            
            mailMsg = EmailMessage(
                'Forgot Password?',
                 html_mail,
                'no-reply@onerooftech.com',
                [email],
                )
            mailMsg.content_subtype ="html"
            mailsend = mailMsg.send()
           
            return Response({"data":{},"response":{"n": 1,"msg":"Email Sent Successfully!", "status":"success" }})
        else:
            return Response({"data":{},"response":{"n": 0,"msg" : "User not found", "status":"error"}})


class setnewpassword(GenericAPIView):
    def post(self,request):
        data={}
        data['id']=request.data.get('id')
        print("id",data['id'])
        empdata = User.objects.filter(id=data['id'],isActive=True).first()
        if empdata is not None:
            data['Password']=request.data.get('Password')
            data['cfpassword']=request.data.get('cfpassword')
            userpassword = data['Password']
            if data['Password'] != data['cfpassword']:
                return Response({"data":{},"response":{"n": 0 ,"msg":"Passwords do not match","status":"passwords do not match"}})
            else:
                data['password']=make_password(userpassword)
                data['textPassword'] = userpassword
                data['PasswordSet'] = True
                serializer = UserSerializer(empdata,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data" : serializer.data,"response":{"n":1,"msg":"Password set Successfully!","status":"success"}})
                else:
                    return Response({"data" : serializer.errors,"response":{"n":0,"msg":"serializer is not valid","status":"failure"}})
        else:
            return Response({ "data":{},"response":{"n":0,"msg":"user not found", "status":"failure"}})


class resetpassword(GenericAPIView):
    
    def post(self,request):
        data={}
        data['id']=request.data.get('id')
        empdata = User.objects.filter(id=data['id'],isActive=True,PasswordSet=True).first()
        if empdata is not None:
            data['Password']=request.data.get('Password')
            data['cfpassword']=request.data.get('cfpassword')
            userpassword = data['Password']
            if data['Password'] != data['cfpassword']:
                return Response({"data":{},"response":{"n": 0 ,"msg":"Passwords do not match","status":"passwords do not match"}})
            else:
                data['password']=make_password(userpassword)
                data['textPassword'] = userpassword
                serializer = UserSerializer(empdata,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data" : serializer.data,"response":{"n":1,"msg":"Password Reset Successfully!","status":"success"}})
                else:
                    return Response({"data" : serializer.errors,"response":{"n":0,"msg":"serializer is not valid","status":"failure"}})
        else:
            return Response({ "data":{},"response":{"n":0,"msg":"user not found", "status":"failure"}})
        
        
      
        
        
        
        
        
        
        
        
        