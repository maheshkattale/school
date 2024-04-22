from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SchoolMaster.models import School
from User.models import User,Role
from User.serializers import UserSerializer
from SchoolMaster.serializers import schoolSerializer
from SchoolMaster.common import createschooladmin
from django.template.loader import get_template, render_to_string



def schoolUniqueCode(schoolname):
    school = [s[0].upper() for s in schoolname.split()]
    schoolJoin = "".join(school)
    firstschool = schoolJoin + "001"
    schoolobject = School.objects.filter(isActive=True).order_by('-createdAt').first()
    if schoolobject is None:
        schoolcode = firstschool
        return schoolcode
    else:
        stripschool = schoolobject.schoolcode[-3:]
        increementschool = int(stripschool) + 1
        placeschool = "%03d" % (increementschool)
        newschoolcode = schoolJoin + str(placeschool)
        return newschoolcode



class AddSchool(GenericAPIView):
    def post(self,request):
        userdata = {}
        data = request.data.copy()
        data['isActive'] = True
        schoolexist = School.objects.filter(Name=data['Name'],isActive= True).first()
        if schoolexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "School Name already exist","status": "failure"}})
        
        Schoolnumberexist = School.objects.filter(Contact=data['Contact'],isActive= True).first()
        if Schoolnumberexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "School Contact already exist","status": "failure"}})
        
        schoolemailexist =  School.objects.filter(Email=data['Email'],isActive= True).first()
        if schoolemailexist is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "School Email already exist","status": "failure"}})
        
        adminemail = School.objects.filter(admin_Email=data['admin_Email'],isActive= True).first()
        if adminemail is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "School Admin Email already exist","status": "failure"}})
        
        useradminemail = User.objects.filter(email=data['admin_Email'],isActive= True).first()
        if useradminemail is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "School Admin Email already exist","status": "failure"}})
        else:
            schoolcode = schoolUniqueCode(data['Name'])
            data['school_code'] = schoolcode
            serializer = schoolSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                createschooladmin(data['admin_Email'],data['admin_Name'],schoolcode)

                # subject = "Set Password"
                # data2 = {"subject": subject,"email":data['admin_Email'],"adminname":data['admin_Name'],
                #     "template": 'mails/sendmailforpassword.html'}
                # message = render_to_string(data2['template'], data2)

                return Response({"data":'',"response": {"n": 1, "msg": "School added successfully","status": "success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "School not added ","status": "failure"}})
          

class schoollist(GenericAPIView):
    def get(self,request):
        schoolobjs = School.objects.filter(isActive=True).order_by('-id')
        serializer = schoolSerializer(schoolobjs,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "school list found successfully","status": "success"}})
       

class getschoolbyid(GenericAPIView):
    def post(self,request):
            id = request.data.get('id')
            schoolobj = School.objects.filter(id=id,isActive=True).first()
            if schoolobj is not None:
                serializer = schoolSerializer(schoolobj)
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "School found successfully","status": "success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "School not found ","status": "failure"}})
            

class updateSchool(GenericAPIView):
    def post(self,request):
        data = request.data.copy()
        schoolid = data['id']
        schoolobj = School.objects.filter(id=schoolid,isActive=True).first()
        if schoolobj is not None:
            schoolexist = School.objects.filter(Name=data['Name'],isActive= True).exclude(id=schoolid).first()
            if schoolexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "school already exist","status": "failure"}})
            
            schoolemailexist =  School.objects.filter(Email=data['Email'],isActive= True).exclude(id=schoolid).first()
            if schoolemailexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "School Email already exist","status": "failure"}})
            
            Schoolnumberexist = School.objects.filter(Contact=data['Contact'],isActive= True).exclude(id=schoolid).first()
            if Schoolnumberexist is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "School Contact already exist","status": "failure"}})
            
            adminemail = School.objects.filter(admin_Email=data['admin_Email'],isActive= True).exclude(id=schoolid).first()
            if adminemail is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "School Admin Email already exist","status": "failure"}})
            
            useradminemail = User.objects.filter(email=data['admin_Email'],isActive= True).exclude(id=schoolid).first()
            if useradminemail is not None:
                return Response({"data":'',"response": {"n": 0, "msg": "School Admin Email already exist","status": "failure"}})

            else:
                serializer = schoolSerializer(schoolobj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "School Updated successfully","status": "success"}})
                else:
                    return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Update School ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "School not found ","status": "failure"}})


class disableSchool(GenericAPIView):
    def post(self,request):
        data = request.data.copy()
        schoolid = data['id']
        schoolobj = School.objects.filter(id=schoolid,isActive=True).first()
        if schoolobj is not None:
            data['isActive'] = False
            schoolcode = schoolobj.school_code
            serializer = schoolSerializer(schoolobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                Userobj = User.objects.filter(school_code=schoolcode,isActive=True).update(isActive=False)
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "School Disabled successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Disable School ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "School not found ","status": "failure"}})


class enableSchool(GenericAPIView):
    def post(self,request):
        data = request.data.copy()
        schoolid = data['id']
        schoolobj = School.objects.filter(id=schoolid,isActive=False).first()
        if schoolobj is not None:
            data['isActive'] = True
            schoolcode = schoolobj.school_code
            serializer = schoolSerializer(schoolobj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                Userobj = User.objects.filter(school_code=schoolcode,isActive=False).update(isActive=True)
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "School Activated successfully","status": "success"}})
            else:
                return Response({"data":serializer.errors,"response": {"n": 0, "msg": "Couldn't Activate School ! ","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "School not found ","status": "failure"}})
