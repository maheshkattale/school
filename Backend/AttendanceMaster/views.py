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
from tablib import Dataset




class mark_class_attendance(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['isActive'] = True
        data['school_code'] =request.user.school_code
        data['class_id'] = request.POST.get('class_id')
        data['Date'] = request.POST.get('Date')
        current_academic_year_obj=AcademicYear.objects.filter(isActive=True,Isdeleted=False,school_code=data['school_code']).first()
        if current_academic_year_obj is not None:
            data['academic_year_id'] = current_academic_year_obj.id
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "Active academic year is not set","status": "failure"}})

        if request.POST.get('student_ids_list') is not None and request.POST.get('student_ids_list') !='':
            data['student_ids_list'] = json.loads(request.POST.get('student_ids_list'))
            for student in data['student_ids_list']:
                dictornary={}
                dictornary['student_id'] = student['student_id']
                if student['IsPresent'] is not None and student['IsPresent'] !='':
                    dictornary['IsPresent'] = student['IsPresent']
                else:
                    dictornary['IsPresent'] = None
                dictornary['school_code'] = data['school_code']
                dictornary['class_id'] = data['class_id']
                dictornary['Date'] = data['Date']
                dictornary['academic_year_id'] = data['academic_year_id']
                print("dictornary",dictornary)


                class_attendance=ClassAttendance.objects.filter(student_id=dictornary['student_id'],school_code=dictornary['school_code'],class_id=dictornary['class_id'],Date=dictornary['Date']).first()
                if class_attendance is not None:
                    dictornary['updatedBy']=str(request.user.id)
                    class_serializer=ClassAttendanceSerializer(class_attendance,data=dictornary,partial=True)
                else:
                    dictornary['createdBy']=str(request.user.id)
                    class_serializer=ClassAttendanceSerializer(data=dictornary)

                if class_serializer.is_valid():
                    class_serializer.save()
                else:
                    print("error",class_serializer.errors)
            return Response({"data":data,"response": {"n": 1, "msg": "Class attendance marked successfully","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "please provide student list","status": "failure"}})





class get_class_attendance_by_date(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = request.data.copy()
        data['school_code'] =request.user.school_code
        data['class_id'] = request.POST.get('class_id')
        data['Date'] = request.POST.get('Date')
        print('data',data)
        current_academic_year_obj=AcademicYear.objects.filter(isActive=True,Isdeleted=False,school_code=data['school_code']).first()
        if current_academic_year_obj is not None:
            data['academic_year_id'] = current_academic_year_obj.id
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "Active academic year is not set","status": "failure"}})

        class_attendance=ClassAttendance.objects.filter(school_code=data['school_code'],class_id=data['class_id'],Date=data['Date'])
        if class_attendance.exists():
            class_serializer=ClassAttendanceSerializer(class_attendance,many=True)

            return Response({"data":class_serializer.data,"response": {"n": 1, "msg": "Class attendance found successfully","status": "success"}})
        else:
            return Response({"data":[],"response": {"n": 0, "msg": "Class attendance not found ","status": "failure"}})























