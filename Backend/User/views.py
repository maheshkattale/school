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

from Parent_StudentMaster.models import *
from Parent_StudentMaster.serializers import *

from .jwt import userJWTAuthentication
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from SchoolErp.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password,check_password
from Frontend.school.static_info import frontend_url

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
                    "data" : {'token':'','username':'','user_id':'','schoolcode':'','Menu':[],'roleid':'','Address':'','mobileNumber':'','email':'','children_list':[],'PrimaryStudentCode':'','PrimaryStudentId':''},
                    "response":{
                    "status":"error",
                    'msg': 'Please provide email and password',
                    'n':0
                    }})
        
        userexist = User.objects.filter(email=email, isActive=True).first()
        if userexist is None:
           return Response(
                    {
                    "data" : {'token':'','username':'','user_id':'','schoolcode':'','Menu':[],'roleid':'','Address':'','mobileNumber':'','email':'','children_list':[],'PrimaryStudentCode':'','PrimaryStudentId':''},
                    "response":{
                    "status":"error",
                    'msg': 'This user is not found',
                    'n':0
                    }}
                           )
        else:
            user_serializer=UserSerializer(userexist)
            p = check_password(Password,userexist.password)
            if p is False:
                return Response(
                    {
                    "data" : {'token':'','username':'','user_id':'','schoolcode':'','Menu':[],'roleid':'','Address':'','mobileNumber':'','email':'','children_list':[],'PrimaryStudentCode':'','PrimaryStudentId':''},
                    "response":{
                    "status":"error",
                    'msg': 'Please enter correct password',
                    'n':0
                    }}
                                
                                )
            else:
                useruuid = str(userexist.id)
                role = userexist.role

                role_id=user_serializer.data['role']

                username = userexist.Username
                schoolcode = userexist.school_code
                Token = createtoken(useruuid,email,source)
                
                psdata = permission.objects.filter(Role_id=role_id).first()
                serializer = permissionserializer(psdata)
               
                menupath=[]
                for i in serializer.data['permission']:
                    menupath.append(i)
             
                permisionobj = MenuItem.objects.filter(MenuID__in = menupath).order_by('SortOrder')
                perSer = MenuItemSerializer(permisionobj,many=True)
                
                if source == "Web":
                    web_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createwebtoken = UserToken.objects.create(User=useruuid,WebToken=Token,source=source)
                elif source == "Mobile":
                    mobile_tokenexist = UserToken.objects.filter(User=useruuid,isActive=True,source=source).update(isActive=False)
                    createmobiletoken = UserToken.objects.create(User=useruuid,MobileToken=Token,source=source)
                else:
                    return Response({
                        "data" : {'token':'','username':'','user_id':'','schoolcode':'','Menu':[],'roleid':'','Address':'','mobileNumber':'','email':'','children_list':[],'PrimaryStudentCode':'','PrimaryStudentId':''},
                        "response":{
                        "status":"error",
                        'msg': 'Please Provide Source',
                        'n':0
                    }
                })
                
                children_list=[]
                PrimaryStudentId = ''
                PrimaryStudentCode =''
                print("user_serializer.data['role']",user_serializer.data['role'])
                if user_serializer.data['role'] == 5:
                    student_objs=Students.objects.filter(ParentId=user_serializer.data['id'],isActive=True,school_code=user_serializer.data['school_code'])
                    children_serializer=StudentSerializer(student_objs,many=True)
                    children_list=children_serializer.data

                    primary_student_objs=Students.objects.filter(ParentId=user_serializer.data['id'],isActive=True,school_code=user_serializer.data['school_code'],primary_student=True).first()
                    if primary_student_objs is not None:
                        PrimaryStudentId = primary_student_objs.id
                        PrimaryStudentCode = primary_student_objs.StudentCode
                        
                return Response({
                    "data" : {'token':Token,'username':username,'user_id':useruuid,'schoolcode':schoolcode,'Menu':perSer.data,'roleid':role_id,'Address':user_serializer.data['Address'],'mobileNumber':user_serializer.data['mobileNumber'],'email':user_serializer.data['email'],'children_list':children_list,'PrimaryStudentCode':PrimaryStudentCode,'PrimaryStudentId':PrimaryStudentId},
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
        menu_list = MenuItem.objects.all().order_by('SortOrder')
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
        psdata = permission.objects.filter(Role_id=roleid)
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
    def post(self,request):
        roleid = request.data.get('roleid')
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
        
        
      
        
        
        

class bulk_upload_fees_distribution(GenericAPIView):

    def post(self,request):
        dataset = Dataset()
        fileerrorlist=[]
        new_product = request.FILES['myfile']

        if not new_product.name.endswith('xlsx'):
            response_={
                'status':'failed',
                'msg':'file format not supported.',
                'data':{}
            }
            return Response(response_,status=200)

        imported_data = dataset.load(new_product.read(), format='xlsx')
        for i in imported_data:
            if i[0] is not None and i[0] !="" and i[2] is not None and i[2]!="":
                data={}
                data['product_name'] = str(i[2])
                data['Ucode'] = i[1]
                productinfoobj = GemstoneProductInfo.objects.filter(product_name__in=[data['product_name'].strip().capitalize(),data['product_name'].strip(),data['product_name'].title()],isActive=True).first()
                if productinfoobj is not None:
                    e1 = 'Product Name Already Exist.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue

                data['product_code'] = str(i[0])
                data['skucode'] = str("SKU") + str(data['product_code'])
                productcodeobj = GemstoneProductInfo.objects.filter(product_code__in=[data['product_code'].strip().capitalize(),data['product_code'].strip(),data['product_code'].title()],isActive=True).first()
                if productcodeobj is not None:
                    e1 = 'product code already exist.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue




                if i[3] is  None or i[3] =="":
                    e1 = 'Gemstone 2nd level  Category required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue

                maincat_obj = GemstoneMainCategory.objects.filter(name__in=[str(i[3]).strip().capitalize(),str(i[3]).strip(),str(i[3]).title()],isActive=True).first()
                if maincat_obj is None:
                    e1 = 'Gemstone 2nd level Category Not Found.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue


                data['main_category'] = maincat_obj.id

                if i[4] is not None and i[4] !="":
                    subcat_obj = GemstoneSubcategory.objects.filter(name__in=[str(i[4]).strip().capitalize(),str(i[4]).strip(),str(i[4]).title()],isActive=True).first()
                    if subcat_obj is None:
                        e1 = 'Gemstone 3rd level Category Not Found.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue


                    data['sub_category'] = subcat_obj.id


                    if subcat_obj.maincategory != maincat_obj.id:
                        e1 = 'Gemstone 3rd level Category is Not related with 2nd level category.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                

                data['short_description'] = i[5]

                data['long_description'] = i[6]

                if i[7] is None or i[7] =="":
                    e1 = 'Thumbnail image is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue
                data['thumbnail_image'] = i[7]
                
                if i[8] is not None and i[8] !="":
                    images = str(i[8]).split(',')
                    images_id_list = []
                    for im in images:
                        imagesobj = S3MediaUpload.objects.filter(file_url=im,isActive=True).first()
                        if imagesobj is None:
                            e1 = 'Images not found.'
                            i_append = i + tuple(e1)
                            fileerrorlist.append(i_append)
                            continue

                        else:
                            images_id_list.append(imagesobj.file_url)
                
                    data['image'] = images_id_list 
                else:
                    e1 = 'Images not found.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue
                # data['image'] = images_id_list 
                
                
                data['origin'] = i[9]

                data['carat_weight'] = i[10]


                ring=''
                if i[11] is not None and i[11] !="":
                    ring  = i[11].split(',')

                ring_id_list = []
                r1=1
                for r in ring:
                    ringobj = GemstoneGroup.objects.filter(name=r,design_type=3,isActive=True).first()
                    if ringobj is None:
                        r1=0
                        e1 = 'ring Not Found'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                    else:
                        ring_id_list.append(ringobj.id)
                if r1 == 0:
                    continue

                data['ring'] = ring_id_list


                pendent=''
                if i[12] is not None and i[12] !="":
                    pendent = i[12].split(',')
                    pendent_id_list = []
                    p1=1
                    for p in pendent:
                        pendentobj = GemstoneGroup.objects.filter(name=p,design_type=2,isActive=True).first()
                        if pendentobj is None:
                            p1=0
                            e1 = 'Pendent Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
                        else:
                            pendent_id_list.append(pendentobj.id)
                    if p1 == 0:
                        continue
                    data['pendent'] = pendent_id_list

                bracelet =''
                if i[13] is not None and i[13] !="":
                    bracelet = i[13].split(',')
                    bracelet_id_list = []
                    b1 =1
                    for b in bracelet:
                        braceletobj = GemstoneGroup.objects.filter(name=b,design_type=1,isActive=True).first()
                        if braceletobj is None:
                            b1=0
                            e1 = 'Braclet Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
                        else:
                            bracelet_id_list.append(braceletobj.id)
                    if b1 == 0:
                        continue
                    data['bracelet'] = bracelet_id_list

                puja_energization=''
                if i[14] is not None and i[14] !="":
                    puja_energization = i[14].split(',')
                    puja_energization_id_list = []
                    for p in puja_energization:
                        pujaenerobj = PujaEnergization.objects.filter(name=p,isActive=True).first()
                        if pujaenerobj is None:
                            e1 = 'Puja Energization Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
                        else:
                            puja_energization_id_list.append(pujaenerobj.id)
                    data['puja_energization'] = puja_energization_id_list

                certification=''
                if i[15] is not None and i[15] !="":
                    certification = i[15].split(',')
                    certification_id_list = []
                    c1=1
                    for c in certification:
                        certificationobj = Certification.objects.filter(name=c,isActive=True).first()
                        if certificationobj is None:
                            c1=0
                            e1 = 'Certification Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
                        else:
                            certification_id_list.append(certificationobj.id)
                    if c1 == 0:
                        continue
                    data['certification'] = certification_id_list



                data['tags'] = i[16]



                if i[17] is None or i[17] =="":
                    e1 = 'Cost Price is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue

                if i[17] is not None and i[17] != "":
                    if not str(i[17]).replace(".", "").isdigit():
                        e1 = 'Cost Price should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[17])
                    if price_float <= 0:
                        e1 = 'Cost Price must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 

                    data['cost_price'] = i[17]


                data['calculation_remark'] = i[18]
                if i[19] is None or i[19] =="":
                    e1 = 'Selling Price is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue
                
                if i[19] is not None and i[19] != "":
                    if not str(i[19]).replace(".", "").isdigit():
                        e1 = 'Selling Price should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[19])
                    if price_float <= 0:
                        e1 = 'Selling Price must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 

                    data['selling_price'] = i[19]

                if i[20] is not None and i[20] !="":

                    if not str(i[20]).replace(".", "").isdigit():
                        e1 = 'Max discount should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[20])
                    if price_float < 0 or price_float>=100:
                        e1 = 'Max discount must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 
                    
                    data['max_discount'] = i[20]
                    mcount = float(data['max_discount'])/100
                    mamount = float(data['selling_price']) * mcount
                    max_discounted_value = float(data['selling_price']) -  mamount
                    data['max_discounted_value'] = max_discounted_value
                else:
                    e1 = 'Max Dicount is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue

                if i[21] is not None and i[21] !="":

                    if not str(i[21]).replace(".", "").isdigit():
                        e1 = 'Wholesale discount should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[21])
                    if price_float < 0 or price_float>=100:
                        e1 = 'Wholesale discount must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 
                    data['wholesale_discount'] = i[21]
                    wcount = float(data['wholesale_discount'])/100
                    wamount = float(data['selling_price']) * wcount
                    wholesale_discount_value = float(data['selling_price']) -  wamount
                    data['wholesale_discount_value'] = wholesale_discount_value
                else:
                    e1 = 'Wholesale Dicount is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue

                if i[22] is not None and i[22] !="":

                    if not str(i[22]).replace(".", "").isdigit():
                        e1 = 'partner discount should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[22])
                    if price_float < 0 or price_float>=100:
                        e1 = 'partner discount must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 
                    data['partner_discount'] = i[22]
                    pcount = float(data['partner_discount'])/100
                    pamount = float(data['selling_price']) * pcount
                    partner_discount_value = float(data['selling_price']) -  pamount
                    data['partner_discount_value'] = partner_discount_value
                else:
                    e1 = 'Partner Dicount is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue


                data['video_upload'] = i[23]
                data['meta_title'] = i[24]
                if i[24] =="" or i[24] is None:
                    data['meta_title'] = data['product_name']
                data['meta_description'] = i[25]
                if i[25] == "" or i[25] is None:
                    data['meta_description'] = data['product_name']




                if i[26] is not None and i[26] !="":

                    main_slug_object = SlugValue.objects.filter(slug_value__in = [str(i[26]).strip().capitalize(),str(i[26]).strip(),str(i[26]).title(),str(i[26]).lower()],isActive= True).first()
                    if str(i[26]).startswith("buy/"):
                        print("The string starts with 'buy/'.")
                    else:
                        e1 = 'Slug Value does not start with buy/.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue

                    if main_slug_object is not None:
                        e1 = 'Slug Value already exists by another product.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                    else:
                        data['slug_value'] = i[26]
                else:
                    e1 = 'Slug Value is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue





                data['header_tag'] = i[27]
                data['schema_tag'] = i[28]
                data['custom_tag'] = i[29]

                manage_shipping=''
                if i[30] is not None and i[30] !="":
                    if (i[30]).lower() == "yes":
                        manage_shipping = True
                    else:
                        manage_shipping = False

                if i[30] is not None and i[30] !="":
                    if (i[30]).lower() != "yes" and (i[30]).lower() != "no":
                        e1 = 'manage shipping must be yes or no.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                    
                    
                data['manage_shipping'] = manage_shipping

                if data['manage_shipping'] == True:
                    data['courier_name'] = i[31]

                    data['courier_weight'] = i[32]
                    if i[32] == "" or i[32] is None:
                        e1 = 'Courier weight is required.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                    if not str(i[32]).replace(".", "").isdigit():
                        e1 = 'Courier weight should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[32])
                    if price_float <= 0:
                        e1 = 'Courier weight must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 




                data['gst_name'] = i[33]
                data['hsn_code'] = i[34]
                if i[34] == "" or i[34] is None:
                    e1 = 'HSN code is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue
                
                
                if i[35] == "" or i[35] is None:
                    e1 = 'GST is required.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue
                if not str(i[35]).replace(".", "").isdigit():
                    e1 = 'GST should only contain digits and a decimal point.'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue   

                price_float = float(i[35])
                if price_float <= 0:
                    e1 = 'GST must be valid'
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue 
                valid_Gst = [0, 0.25, 3, 5, 12, 18, 28]
                if int(i[35]) in valid_Gst:
                    data['gst'] = i[35]
                else:
                    e1 = 'GST  must be 0, 0.25, 3, 5, 12, 18, 28 '
                    i_append = i + tuple([e1])
                    fileerrorlist.append(i_append)
                    continue  
                data['gst'] = i[35]



                manage_inventory=''


                if i[36] is not None and i[36] !="":
                    if (i[36]).lower() == "yes":
                        manage_inventory = True
                    else:
                        manage_inventory = False
                data['manage_inventory'] = manage_inventory
                if data['manage_inventory'] ==True:


                    if i[37] == "" or i[37] is None:
                        e1 = 'Current Stock is required.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue
                    if not str(i[37]).replace(".", "").isdigit():
                        e1 = 'Current Stock should only contain digits and a decimal point.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue   

                    price_float = float(i[37])
                    if price_float < 0:
                        e1 = 'Current Stock must be valid'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue 
                    data['current_stock'] = i[37]


                    data['warehouse'] = i[38]

                if data['carat_weight'] is not None and data['carat_weight'] != "":
                    data['ratti_weight'] = round((float(data['carat_weight'])*0.91),2)


                if i[39] is not None and i[39] !="":
                    vendor = i[39].split(',')
                    vendor_id_list = []
                    v1=1
                    for c in vendor:
                        vendorobj = Vendor.objects.filter(vendor_name=c,isActive=True).first()
                        if vendorobj is None:
                            v1=0
                            e1 = 'Vendor Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
                        else:
                            vendor_id_list.append(vendorobj.id)
                    if v1 == 0:
                        continue
                    data['vendor'] = vendor_id_list


                if i[40] is not None and i[40] !="":
                    team = i[40].split(',')
                    team_id_list = []
                    t1=1
                    for c in team:
                        teamobj = Team.objects.filter(name=c,isActive=True).first()
                        if teamobj is None:
                            t1=0
                            e1 = 'Team Not Found.'
                            i_append = i + tuple([e1])
                            fileerrorlist.append(i_append)
                            continue
 
                        else:
                            team_id_list.append(teamobj.id)
                    if t1 == 0:
                        continue
                    data['team'] = team_id_list
                if i[41] is not None and i[41] !="":
                    data['price_per_carat'] = i[41]
                
                if i[42] is not None and i[42] != "":
                    item_object = Item_type.objects.filter(isActive=True,name=i[42]).first()
                    if item_object is not None:
                        data['item_type'] = i[42]
                    else:
                        e1 = 'Item type Not Found.'
                        i_append = i + tuple([e1])
                        fileerrorlist.append(i_append)
                        continue

                if i[43] is not None and i[43] !="":
                    data['reorder_level'] = i[43]

                if i[44] is not None and i[44] !="":
                    data['sourcing_time'] = i[44]

                infinite_stock = False
                if i[45] is not None and i[45] !="":
                    if (i[45]).lower() == "yes":
                        infinite_stock = True
                    else:
                        infinite_stock = False
                
                data['infinite_stock_status'] = infinite_stock

                serializer = GemstoneProductInfoSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                    created_by = request.session.get('user_id')
                    if i[37] is not None and i[37] != "":
                        purchaseinventoryhistory = ProductInventoryHistory.objects.create(
                        createdBy=created_by,
                        main_prod_type=2,
                        product_id=serializer.data['id'],
                        product_variation = False,
                        product_variation_id =0,
                        sku_code = serializer.data['skucode'],
                        log_type = "Opening Stock",
                        order_id = "Bulk upload Product",
                        transaction_type = "Add",
                        quantity = int(i[37])
                    )

                    slug_object = SlugValue.objects.create(slug_id=serializer.data['id'],slug_value= serializer.data['slug_value'],mainprodtype=2,level=4)
                    for p in images_id_list:
                            GemstoneProductImages.objects.create(productid=serializer.data['id'],image=p)

                    
                else:
                    fileerrorlist.append(i)
                    continue
        response_={
                    'status':'success',
                    'msg':'Product Added Successfully.',
                    # 'data':serializer.data,
                    'errordata':fileerrorlist
                }
        return Response(response_,status=200)
    

        
        
        
        
        