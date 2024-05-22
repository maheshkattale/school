from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from User.jwt import userJWTAuthentication
from User.models import *
from rest_framework import permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from Parent_StudentMaster.models import Students


class add_message(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        data['from_user_id']=request.POST.get('from_user_id')
        print("data",request.data)
        school_code=request.user.school_code
        from_user_obj=User.objects.filter(id=data['from_user_id'],isActive=True).first()
        if from_user_obj is None:
            return Response({"data":'',"response": {"n": 0, "msg":'from user not found',"status": "failure"}})
        
        if str(from_user_obj.role) == 'Parent':
            
            student_obj=Students.objects.filter(StudentCode=request.POST.get('StudentCode'),school_code=school_code,ParentId=from_user_obj.id,isActive=True).first()
            if student_obj is not None:
                data['StudentCode']=student_obj.StudentCode
            else:
                return Response({"data":'',"response": {"n": 0, "msg":'we dont found your student ',"status": "failure"}})
        # print("from_user_obj",str(from_user_obj.role))

        data['from_user_str']=from_user_obj.Username
        data['message']=request.POST.get('message')
        data['short_message']=request.POST.get('subject')
        
        data['to_user_id']=request.POST.get('to_user_id')
        to_user_obj=User.objects.filter(id=data['to_user_id'],isActive=True).first()
        if to_user_obj is None:
            return Response({"data":'',"response": {"n": 0, "msg":'To user not found',"status": "failure"}})
        
        if str(to_user_obj.role) == 'Parent':
            # print("to_user_obj.id",to_user_obj.id)
            # print("school_code",school_code)
            
            student_obj=Students.objects.filter(StudentCode=request.POST.get('StudentCode'),school_code=school_code,ParentId=to_user_obj.id,isActive=True).first()
            # print("student_obj",student_obj)
            
            if student_obj is not None:
                data['StudentCode']=student_obj.StudentCode
            else:
                return Response({"data":'',"response": {"n": 0, "msg":'we dont found your student ',"status": "failure"}})
        # print("to_user_obj",str(to_user_obj.role))

        data['to_user_str']=to_user_obj.Username

        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        data['date_str']=formatted_date
        data['school_code']=school_code
        
        # print("data",data)
        serializer=MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message Added Successfully","status": "Success"}})
        else:
            first_key, first_value = next(iter(serializer.errors.items()))
            return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})

class edit_message(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
       

        message_id=request.POST.get('id')
        data['message']=request.POST.get('message')
        data['short_message']=request.POST.get('subject')
        
        message_obj=Messages.objects.filter(id=message_id,isActive=True).first()
        if message_obj is not None:
            
            serializer=MessageSerializer(message_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message updated Successfully","status": "Success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg":'message not found',"status": "failure"}})
            
class get_send_messages(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):   
        user_id=request.user.id
        print("request.user.role",request.user.role)
        print("request.POST.get('StudentCode')",request.POST.get('StudentCode'))
        # print("user_id",user_id)

        message_obj=Messages.objects.filter(from_user_id=user_id,isActive=True)

        if str(request.user.role) == 'Parent':
            if request.POST.get('StudentCode') is not None and request.POST.get('StudentCode') !="":
                
                student_obj=Students.objects.filter(StudentCode=request.POST.get('StudentCode'),ParentId=user_id,isActive=True).first()
                if student_obj is not None:
                    message_obj=message_obj.filter(StudentCode=student_obj.StudentCode)
                else:
                    return Response({"data":'',"response": {"n": 0, "msg":'we dont found your student ',"status": "failure"}})
            else: 
                return Response({"data":'',"response": {"n": 0, "msg":'please provide student code ',"status": "failure"}})
                
            
            
        serializer=CustomMessageSerializer(message_obj,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message found Successfully","status": "Success"}})
   
class get_recived_messages(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):   
        user_id=request.user.id
        # print("user_id",user_id)
        message_obj=Messages.objects.filter(to_user_id=user_id,isActive=True)
        serializer=CustomMessageSerializer(message_obj,many=True)
        return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message found Successfully","status": "Success"}})

class delete_message(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
       
        message_id=request.POST.get('id')
        data['isActive']=False
        message_obj=Messages.objects.filter(id=message_id,isActive=True).first()
        if message_obj is not None:
            serializer=MessageSerializer(message_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message deleted Successfully","status": "Success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg":'message not found',"status": "failure"}})
            
class get_recipients(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        
        # if request.user.role == "Parent":
            
        data={}
        message_id=request.POST.get('id')
        data['isActive']=False
        message_obj=Messages.objects.filter(id=message_id,isActive=True).first()
        if message_obj is not None:
            serializer=MessageSerializer(message_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message deleted Successfully","status": "Success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg":first_key + ' : '+first_value[0],"status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg":'message not found',"status": "failure"}})
            












        
