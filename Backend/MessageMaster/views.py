from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from User.jwt import userJWTAuthentication
from User.models import *
from rest_framework import permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from Parent_StudentMaster.models import *
from Parent_StudentMaster.serializers import *
from NotificationMaster.models import *
from NotificationMaster.serializers import *
class add_message(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        school_code=request.user.school_code
        data['from_user_id']=str(request.user.id)
        data['from_user_str']=request.user.Username
        from_user_studentcode=request.POST.get('from_user_studentcode')
        from_user_studentid=''
        if from_user_studentcode is not None and from_user_studentcode !='':
            student_obj=Students.objects.filter(StudentCode=from_user_studentcode,school_code=school_code,isActive=True).first()
            if student_obj is not None:
                data['from_user_studentcode']=student_obj.StudentCode
                from_user_studentid=student_obj.id
            else:
                return Response({"data":'',"response": {"n": 0, "msg":'we dont found your student ',"status": "failure"}})

        data['message']=request.POST.get('message')
        data['short_message']=request.POST.get('subject')
        
        data['to_user_id']=request.POST.get('to_user_id')
        to_user_obj=User.objects.filter(id=data['to_user_id'],isActive=True,school_code=school_code).first()
        if to_user_obj is None:
            return Response({"data":'',"response": {"n": 0, "msg":'To user not found',"status": "failure"}})
        to_user_studentid=''
        to_user_studentcode=request.POST.get('to_user_studentcode')
        if to_user_studentcode is not None and to_user_studentcode !='':
            student_obj=Students.objects.filter(StudentCode=to_user_studentcode,school_code=school_code,isActive=True).first()
            if student_obj is not None:
                data['to_user_studentcode']=student_obj.StudentCode
                to_user_studentid=student_obj.id
            else:
                return Response({"data":'',"response": {"n": 0, "msg":'we dont found to user student ',"status": "failure"}})
        data['to_user_str']=to_user_obj.Username
        current_date = datetime.now().strftime('%Y-%m-%d')
        data['date_str']=current_date
        data['school_code']=school_code
        
        serializer=MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            notification_data={}
            
            notification_data['to_user']=str(serializer.data['to_user_id'])
            notification_data['to_user_studentid']=str(to_user_studentid)
            notification_data['from_user']=str(serializer.data['from_user_id'])
            notification_data['from_user_studentid']=str(from_user_studentid)
            notification_data['notification_title']=str(serializer.data['short_message'])
            notification_data['notification_message']=str(serializer.data['message'])
            notification_data['notification_type']=str(1)
            notification_data['school_code']=str(school_code)
            
            
            notification_serializer=NotificationMasterSerializer(data=notification_data)
            if notification_serializer.is_valid():
                notification_serializer.save()
            else:
                print("notifi",notification_serializer.errors)
                
                
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Message send successfully","status": "Success"}})
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
        message_obj=Messages.objects.filter(from_user_id=user_id,isActive=True)
        if str(request.user.role) == 'Parent':
            if request.POST.get('StudentCode') is not None and request.POST.get('StudentCode') !="":
                student_obj=Students.objects.filter(StudentCode=request.POST.get('StudentCode'),ParentId=user_id,isActive=True).first()
                if student_obj is not None:
                    message_obj=message_obj.filter(from_user_studentcode=student_obj.StudentCode)
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
        message_obj=Messages.objects.filter(to_user_id=user_id,isActive=True)
        if str(request.user.role) == 'Parent':
            if request.POST.get('StudentCode') is not None and request.POST.get('StudentCode') !="":
                student_obj=Students.objects.filter(StudentCode=request.POST.get('StudentCode'),ParentId=user_id,isActive=True).first()
                if student_obj is not None:
                    message_obj=message_obj.filter(to_user_studentcode=student_obj.StudentCode)
                else:
                    return Response({"data":'',"response": {"n": 0, "msg":'we dont found your student ',"status": "failure"}})
            else: 
                return Response({"data":'',"response": {"n": 0, "msg":'please provide student code ',"status": "failure"}})
        
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
            
class check_recipient_type(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        user_id=request.POST.get('id')
        school_code=request.user.school_code
        user_obj=User.objects.filter(id=user_id,isActive=True,school_code=school_code).first()
        if user_obj is not None:
            if str(user_obj.role) == 'Parent':
                studentlist_obj=Students.objects.filter(ParentId=user_obj.id,isActive=True,school_code=school_code)
                if studentlist_obj.exists():
                    serializer=StudentSerializer(studentlist_obj,many=True)
                    return Response({"data":serializer.data,"response": {"n": 1, "msg": "This user is a parent user","status": "Success"}})
                else:
                    return Response({"data":[],"response": {"n": 0, "msg": "This user is a parent user but dont have any childs","status": "failure"}})
            else:
                return Response({"data":[],"response": {"n": 0, "msg":'This user is not parent user',"status": "failure"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg":'User not found',"status": "failure"}})
            












        
