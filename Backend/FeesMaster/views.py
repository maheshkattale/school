from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from SubjectMaster.models import Subject
from TeacherMaster.models import TeacherSubject
from TeacherMaster.serializers import *
from SubjectMaster.serializers import SubjectSerializer
from User.models import User
from User.serializers import UserSerializer,UserlistSerializer
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from User.jwt import userJWTAuthentication
from rest_framework import permissions
from .models import *
from .serializers import *
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER
from datetime import datetime, timedelta
from Parent_StudentMaster.models import Students,studentclassLog
from Parent_StudentMaster.serializers import *
from tablib import Dataset
from SchoolMaster.models import AcademicYear
from ClassMaster.models import Class
from Frontend.school.custom_function import *

class bulk_upload_fees_distribution(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        dataset = Dataset()
        school_code=request.user.school_code
        fileerrorlist=[]
        new_fees_distributions = request.FILES['file']

        if not new_fees_distributions.name.endswith('xlsx'):
            return Response({'data':[],"response":{"status":"failure",'msg': 'file format not supported','n':0}})
        imported_data = dataset.load(new_fees_distributions.read(), format='xlsx')
        for i in imported_data:
            if i[0] is not None and i[0] !="":
                data={}
                data['acedamic_dates'] = str(i[0])
                data['valid_entry']=True
                data['breakdown']=False

                if data['acedamic_dates'] is not None and data['acedamic_dates'] !='':
                    dates = data['acedamic_dates'].split(' ')
                    if len(dates) == 2:
                        if is_valid_dd_mm_yyyy(dates[0]):
                            start_date=dd_mm_yyyy_to_yyyy_mm_dd(dates[0])
                            if is_valid_dd_mm_yyyy(dates[1]):
                                end_date=dd_mm_yyyy_to_yyyy_mm_dd(dates[1])

                                AcademicYear_obj=AcademicYear.objects.filter(startdate=str(start_date),enddate=str(end_date),Isdeleted=False,school_code=school_code).first()
                                if AcademicYear_obj is not None:
                                    data['academic_year_id']=AcademicYear_obj.id
                                else:
                                    data['valid_entry']=False
                                    reason = 'Academic year with this dates not found.'
                                    error = i + tuple([reason])
                                    fileerrorlist.append(error)
                                    continue
                            else:
                                data['valid_entry']=False
                                reason = 'valid start dates and end dates  required.'
                                error = i + tuple([reason])
                                fileerrorlist.append(error)
                                continue
                        else:
                            data['valid_entry']=False
                            reason = 'valid start dates and end dates  required.'
                            error = i + tuple([reason])
                            fileerrorlist.append(error)
                            continue
                    else:
                        data['valid_entry']=False
                        reason = 'valid start dates and end dates required.'
                        error = i + tuple([reason])
                        fileerrorlist.append(error)
                        continue
                else:
                    data['valid_entry']=False
                    reason = 'academic year dates required.'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue
                
                data['class_name'] = str(i[1]).lower()
                if data['class_name'] is not None and data['class_name'] !='':
                    
                    class_obj=Class.objects.filter(ClassName__icontains=data['class_name'],isActive=True).first()
                    if class_obj is not None :
                        data['class_id']=class_obj.id
                    else:
                        data['valid_entry']=False
                        reason = 'class with this class name not found'
                        error = i + tuple([reason])
                        fileerrorlist.append(error)
                        continue
                else:
                    data['valid_entry']=False
                    reason = 'Please enter a valid class'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue
                
                
                if is_valid_number(i[2]):
                    data['total_amount'] = str(i[2])
                else:
                    data['valid_entry']=False
                    reason = 'Please enter a valid total amount number'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue
                
                if is_valid_number(i[3]):
                    data['breakdown_count'] = str(i[3])
                else:
                    data['valid_entry']=False
                    reason = 'Please enter a valid fees breakdown count ,if no breakdown enter 0'
                    error = i + tuple([reason])
                    fileerrorlist.append(error)
                    continue
                iteration_range=int(int(data['breakdown_count'])*4)+3
                
                data['breakdown_list']=[]
                
                
                breakdown_items=['','name','amount','start_date','end_date']
                
                if int(data['breakdown_count']) >=1:
                    iteration_break=0
                    iteration=1
                    single_breakdown={}
                    valid_entry=True

                    for j in range(iteration_range):
                        column_number=j+1
                        if j > 2:
                            iteration_break+=1
                            
                            if iteration_break > 4:
                                iteration_break=1
                                iteration+=1
                                valid_entry=True

                                
                            if i[column_number] is not None and i[column_number] !='':
                                if iteration_break == 1:
                                    single_breakdown[breakdown_items[iteration_break]]=i[column_number]
                                    
                                if iteration_break == 2:
                                    if is_valid_number(i[column_number]):
                                        single_breakdown[breakdown_items[iteration_break]]=i[column_number]
                                    else:
                                        valid_entry=False
                                        data['valid_entry']=False
                                        reason = 'Please enter a valid  breakdown '+ str(iteration) +'  '+ breakdown_items[iteration_break]
                                        error = i + tuple([reason])
                                        fileerrorlist.append(error)
                                        continue
                                if iteration_break == 3 or iteration_break == 4:  
                                    d1=str(i[column_number]).split(' ')[0]
                                    if is_valid_yyyy_mm_dd(str(d1)):
                                        single_breakdown[breakdown_items[iteration_break]]=str(d1)
                                    else:
                                        valid_entry=False
                                        data['valid_entry']=False

                                        reason = 'Please enter a valid  breakdown '+ str(iteration) +'  '+ breakdown_items[iteration_break]
                                        error = i + tuple([reason])
                                        fileerrorlist.append(error)
                                        continue
                            else:
                                valid_entry=False
                                data['valid_entry']=False

                                reason = 'Please enter a valid  breakdown '+ str(iteration) +'  '+breakdown_items[iteration_break]
                                error = i + tuple([reason])
                                fileerrorlist.append(error)
                                continue
                            
                            if iteration_break == 4:
                                if valid_entry==True:
                                    data['breakdown_list'].append(single_breakdown)
                                single_breakdown={}
                            
                            
                            
                            
                if len(data['breakdown_list']) >=1:
                    data['breakdown']=True
                    breakdown_total_amount=0
                    for entry in data['breakdown_list']:
                        breakdown_total_amount+=int(entry['amount'])
                    if int(data['total_amount'])  !=   breakdown_total_amount:
                        data['valid_entry']=False
                        reason = 'fees total amount breakdown is not valid ,sum of breakdown amount must equal to total amount of academic fees'
                        error = i + tuple([reason])
                        fileerrorlist.append(error)
                        continue
                    
                if data['valid_entry']:

                    check_already_exist_obj=FeesDistributions.objects.filter(class_id=data['class_id'],academic_year_id=data['academic_year_id']).first()
                    if check_already_exist_obj is not None:
                        FeesDistributionsSerializers=FeesDistributionsSerializer(check_already_exist_obj,data=data,partial=True)
                    else:
                        FeesDistributionsSerializers=FeesDistributionsSerializer(data=data)
                    if FeesDistributionsSerializers.is_valid():
                        FeesDistributionsSerializers.save()

                        delete_already_exist_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=FeesDistributionsSerializers.data['id']).update(isActive=False)
                        
                        for breakdown in data['breakdown_list']:
                            breakdown['fees_distributions_id']=FeesDistributionsSerializers.data['id']
                            FeesDistributionsBreakdownsSerializers=FeesDistributionsBreakdownsSerializer(data=breakdown)
                            if FeesDistributionsBreakdownsSerializers.is_valid():
                                FeesDistributionsBreakdownsSerializers.save()
                            else:
                                first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                                reason = 'Error in adding fees  breakdown '+first_key +' : '+ first_value[0]
                                error = i + tuple([reason])
                                fileerrorlist.append(error)
                                continue
                    else:
                        first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                        reason = 'Error in adding fees  '+first_key +' : '+ first_value[0]
                        error = i + tuple([reason])
                        fileerrorlist.append(error)
                        continue
        response_={
                    'status':'success',
                    'msg':'Product Added Successfully.',
                    'errorfile':fileerrorlist
                }
        return Response(response_,status=200)
    
    
    
class add_fees_distributions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        breakdown_list = json.loads(data['breakdown_list'])
        check_already_exist_obj=FeesDistributions.objects.filter(class_id=data['class_id'],academic_year_id=data['academic_year_id']).first()
        if check_already_exist_obj is not None:
            return Response({"data":'',"response": {"n": 0, "msg": "fees of this class and academic already exist","status": "failure"}})
        else:
            FeesDistributionsSerializers=FeesDistributionsSerializer(data=data)
            if FeesDistributionsSerializers.is_valid():
                FeesDistributionsSerializers.save()
                if FeesDistributionsSerializers.data['breakdown']:
                    for breakdown in breakdown_list:
                        breakdown['fees_distributions_id']=FeesDistributionsSerializers.data['id']
                        FeesDistributionsBreakdownsSerializers=FeesDistributionsBreakdownsSerializer(data=breakdown)
                        if FeesDistributionsBreakdownsSerializers.is_valid():
                            FeesDistributionsBreakdownsSerializers.save()
                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": 'Error in adding fees breakdown '+first_key +' : '+ first_value[0],"status": "failure"}})
                return Response({"data":'',"response": {"n": 1, "msg": "fees added successfully","status": "success"}})

            else:
                first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg": 'Error in adding fees  '+first_key +' : '+ first_value[0],"status": "failure"}})


class update_fees_distributions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        breakdown_list = json.loads(data['breakdown_list'])
        
        update_obj=FeesDistributions.objects.filter(id=data['id']).first()
        if update_obj is not None:
            FeesDistributionsSerializers=FeesDistributionsSerializer(update_obj,data=data,partial=True)
            if FeesDistributionsSerializers.is_valid():
                FeesDistributionsSerializers.save()
                if FeesDistributionsSerializers.data['breakdown']:
                    delete_already_exist_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=FeesDistributionsSerializers.data['id']).update(isActive=False)

                    for breakdown in breakdown_list:
                        breakdown['fees_distributions_id']=FeesDistributionsSerializers.data['id']
                        FeesDistributionsBreakdownsSerializers=FeesDistributionsBreakdownsSerializer(data=breakdown)
                        if FeesDistributionsBreakdownsSerializers.is_valid():
                            FeesDistributionsBreakdownsSerializers.save()
                        else:
                            return Response({"data":'',"response": {"n": 0, "msg": 'Error in adding fees breakdown '+first_key +' : '+ first_value[0],"status": "failure"}})
                return Response({"data":'',"response": {"n": 1, "msg": "fees updated successfully","status": "success"}})

            else:
                first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg": 'Error in updating fees  '+first_key +' : '+ first_value[0],"status": "failure"}})

        return Response({"data":'',"response": {"n": 0, "msg": "fees  not found","status": "failure"}})

class delete_fees_distributions(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        data['isActive']=False
        
        delete_obj=FeesDistributions.objects.filter(id=data['id'],isActive=True).first()
        if delete_obj is not None:
            FeesDistributionsSerializers=FeesDistributionsSerializer(delete_obj,data=data,partial=True)
            if FeesDistributionsSerializers.is_valid():
                FeesDistributionsSerializers.save()
                delete_already_exist_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=FeesDistributionsSerializers.data['id']).update(isActive=False)
                return Response({"data":'',"response": {"n": 1, "msg": "fees deleted successfully","status": "success"}})
            else:
                first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg": 'Error in deleting fees  '+first_key +' : '+ first_value[0],"status": "failure"}})

        return Response({"data":'',"response": {"n": 0, "msg": "fees not found","status": "failure"}})

class add_fees_distributions_for_multiple_class(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        breakdown_list = json.loads(data['breakdown_list'])
        classes = json.loads(data['classes'])
        if len(breakdown_list) >0:
            data['breakdown']=True
        else:
            data['breakdown']=False
            
  
        not_added_list=[]
        for i in classes:
            data['class_id']=i
            data['isActive']=True
            check_already_exist_obj=FeesDistributions.objects.filter(class_id=i,academic_year_id=data['academic_year_id']).first()
            if check_already_exist_obj is not None:
                not_added_list.append(i)
            else:
                FeesDistributionsSerializers=FeesDistributionsSerializer(data=data)
                if FeesDistributionsSerializers.is_valid():
                    FeesDistributionsSerializers.save()
                    
                    if FeesDistributionsSerializers.data['breakdown']:
                        for breakdown in breakdown_list:
                            breakdown['fees_distributions_id']=FeesDistributionsSerializers.data['id']
                            breakdown['start_date']=dd_mm_yyyy_to_yyyy_mm_dd(breakdown['start_date'])
                            breakdown['end_date']=dd_mm_yyyy_to_yyyy_mm_dd(breakdown['end_date'])
                            FeesDistributionsBreakdownsSerializers=FeesDistributionsBreakdownsSerializer(data=breakdown)
                            if FeesDistributionsBreakdownsSerializers.is_valid():
                                FeesDistributionsBreakdownsSerializers.save()
                            else:
                                print('error',FeesDistributionsBreakdownsSerializers.errors)
                else:
                    not_added_list.append(i)
                    print('error',FeesDistributionsSerializers.errors)
                    
        return Response({"data":'',"response": {"n": 1, "msg": "fees added successfully","status": "success"}})

                    
 
class fees_destributiom_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):        
        obj=FeesDistributions.objects.filter(isActive=True)
        FeesDistributionsSerializers=CustomFeesDistributionsSerializer(obj,many=True)
        newlist=FeesDistributionsSerializers.data
        for i in newlist:
            Breakdowns_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=i['id'],isActive=True)
            Breakdowns_serializer=CustomFeesDistributionsBreakdownsSerializer(Breakdowns_obj,many=True)
            i['Breakdowns']=Breakdowns_serializer.data
        return Response({"data":newlist,"response": {"n": 1, "msg": "fees list found successfully","status": "success"}})
 
                   
class get_fees_distributions_details(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()        
        obj=FeesDistributions.objects.filter(id=data['id'],isActive=True).first()
        if obj is not None:
            FeesDistributionsSerializers=FeesDistributionsSerializer(obj)
            Breakdowns_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=FeesDistributionsSerializers.data['id'],isActive=True)
            Breakdowns_serializer=CustomFeesDistributionsBreakdownsSerializer(Breakdowns_obj,many=True)
            return Response({"data":{'fees':FeesDistributionsSerializers.data,'breakdowns':Breakdowns_serializer.data},"response": {"n": 1, "msg": "fees details found successfully","status": "success"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "fees not found","status": "failure"}})


class edit_fees_distributions_for_multiple_class(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        breakdown_list = json.loads(data['breakdown_list'])
        if data['breakdown'] =='true':
            data['breakdown']=True
        else:
            data['breakdown']=False
            


        data['isActive']=True
        obj=FeesDistributions.objects.filter(class_id=data['class_id'],academic_year_id=data['academic_year_id'],isActive=True).first()
        if obj is not None:
            FeesDistributionsSerializers=FeesDistributionsSerializer(obj,data=data)
            if FeesDistributionsSerializers.is_valid():
                FeesDistributionsSerializers.save()
                if FeesDistributionsSerializers.data['breakdown']:
                    deleteexist=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=int(FeesDistributionsSerializers.data['id'])).update(isActive=False)
                    
                    for breakdown in breakdown_list:
                        breakdown['fees_distributions_id']=FeesDistributionsSerializers.data['id']
                        breakdown['start_date']=dd_mm_yyyy_to_yyyy_mm_dd(breakdown['start_date'])
                        breakdown['end_date']=dd_mm_yyyy_to_yyyy_mm_dd(breakdown['end_date'])
                        FeesDistributionsBreakdownsSerializers=FeesDistributionsBreakdownsSerializer(data=breakdown)
                        if FeesDistributionsBreakdownsSerializers.is_valid():
                            FeesDistributionsBreakdownsSerializers.save()
                        else:
                            print('error',FeesDistributionsBreakdownsSerializers.errors)
                return Response({"data":'',"response": {"n": 1, "msg": "fees  updated Successfully","status": "success"}})
                            
            else:
                print('error',FeesDistributionsSerializers.errors)
                first_key, first_value = next(iter(FeesDistributionsSerializers.errors.items()))
                return Response({"data":'',"response": {"n": 0, "msg": first_key +' : '+ first_value[0],"status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "fees not updated ","status": "failure"}})

        



class get_student_pending_fees_list(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        student_obj=Students.objects.filter(StudentCode=data['StudentCode'],isActive=True,school_code=data['school_code']).first()
        if student_obj is not None:
            student_serializer=StudentSerializer(student_obj)
            class_log_obj=studentclassLog.objects.filter(studentId=student_serializer.data['id'],isActive=True)
            if class_log_obj.exists():
                classIds=studentclassLogserializer(class_log_obj,many=True)
                student_feeslist=[]
                pending_student_feeslist=[]
                paid_student_feeslist=[]
                for i in classIds.data:
                    fees_object=FeesDistributions.objects.filter(class_id=i['classid'],academic_year_id=i['AcademicyearId']).first()
                    if fees_object is not None:
                        fees_distribution_serializers=CustomFeesDistributionsSerializer(fees_object)
                        Breakdowns_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=fees_distribution_serializers.data['id'],isActive=True)
                        Breakdowns_serializer=CustomFeesDistributionsBreakdownsSerializer(Breakdowns_obj,many=True)
                        student_feeslist.append({'fees':fees_distribution_serializers.data,'breakdowns':Breakdowns_serializer.data,'student':student_serializer.data})
                        
                        
                for fees in student_feeslist:
                    check_payment_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id'])
                    fees['fees']['status']='Pay Now'
                    if check_payment_obj.exists():  
                        if fees['fees']['breakdown']==True:
                            un_paid=False
                            for breakdown in fees['breakdowns']:
                                check_payment_breakdowns_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id'],termid=breakdown['id']).first()
                                if check_payment_breakdowns_obj is not None:
                                    breakdown['Paid']=True
                                else:
                                    un_paid=True
                                    breakdown['Paid']=False
                            if un_paid:
                                pending_student_feeslist.append(fees)
                            else:
                                fees['fees']['status']='Paid'
                                paid_student_feeslist.append(fees)
                        else:
                            check_payment_status_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id']).first()
                            if check_payment_status_obj is None:
                                pending_student_feeslist.append(fees)
                            else:
                                fees['fees']['status']='Paid'
                                paid_student_feeslist.append(fees)
                        

        
                    else:
                        pending_student_feeslist.append(fees)
                return Response({"data":pending_student_feeslist+paid_student_feeslist,"response": {"n": 1, "msg": "fees found successfully","status": "success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "student class not found","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student not found","status": "failure"}})


class get_student_pending_fees_list_by_id(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        student_obj=Students.objects.filter(id=data['id'],isActive=True,school_code=data['school_code']).first()
        if student_obj is not None:
            student_serializer=CustomStudentSerializer(student_obj)
            class_log_obj=studentclassLog.objects.filter(studentId=student_serializer.data['id'],isActive=True)
            if class_log_obj.exists():
                classIds=studentclassLogserializer(class_log_obj,many=True)
                student_feeslist=[]
                pending_student_feeslist=[]
                paid_student_feeslist=[]
                for i in classIds.data:
                    fees_object=FeesDistributions.objects.filter(class_id=i['classid'],academic_year_id=i['AcademicyearId']).first()
                    if fees_object is not None:
                        fees_distribution_serializers=CustomFeesDistributionsSerializer(fees_object)
                        Breakdowns_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=fees_distribution_serializers.data['id'],isActive=True)
                        Breakdowns_serializer=CustomFeesDistributionsBreakdownsSerializer(Breakdowns_obj,many=True)
                        student_feeslist.append({'fees':fees_distribution_serializers.data,'breakdowns':Breakdowns_serializer.data,'student':student_serializer.data})
                        
                        
                for fees in student_feeslist:
                    check_payment_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id'])
                    fees['fees']['status']='Pay Now'
                    if check_payment_obj.exists():  
                        if fees['fees']['breakdown']==True:
                            un_paid=False
                            for breakdown in fees['breakdowns']:
                                check_payment_breakdowns_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id'],termid=breakdown['id']).first()
                                if check_payment_breakdowns_obj is not None:
                                    breakdown['Paid']=True
                                else:
                                    un_paid=True
                                    breakdown['Paid']=False
                            if un_paid:
                                pending_student_feeslist.append(fees)
                            else:
                                fees['fees']['status']='Paid'
                                paid_student_feeslist.append(fees)
                        else:
                            check_payment_status_obj=StudentFeesLog.objects.filter(fees_distributions_id=fees['fees']['id'],student_id=fees['student']['id'],class_id=fees['fees']['class_id_id']).first()
                            if check_payment_status_obj is None:
                                pending_student_feeslist.append(fees)
                            else:
                                fees['fees']['status']='Paid'
                                paid_student_feeslist.append(fees)
                        

        
                    else:
                        pending_student_feeslist.append(fees)
                return Response({"data":pending_student_feeslist+paid_student_feeslist,'student':student_serializer.data,"response": {"n": 1, "msg": "fees found successfully","status": "success"}})
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "student class not found","status": "failure"}})
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "student not found","status": "failure"}})



class pay_student_fees(GenericAPIView):
    authentication_classes=[userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data=request.data.copy()
        data['school_code']=request.user.school_code
        data['isActive']=True
        data['termid']=json.loads(request.POST.get('termid'))
        student_obj=Students.objects.filter(StudentCode=data['StudentCode'],isActive=True,school_code=data['school_code']).first()
        class_obj=Class.objects.filter(id=data['class_id'],isActive=True).first()
        successfull_payments=[]
        unsuccessfull_payments=[]

        if student_obj is not None:
            student_serializer=StudentSerializer(student_obj)
            data['student_id']=student_serializer.data['id']
            if class_obj is not None:
                FeesDistributions_obj=FeesDistributions.objects.filter(id=data['fees_distributions_id'],isActive=True).first()
                if FeesDistributions_obj is not None:
                    if data['termid']=='' or data['termid'] is None or data['termid'] == []:
                        if FeesDistributions_obj.breakdown == True:
                            # want to make make full payment of all breakdowns
                            get_breakdown_obj=FeesDistributionsBreakdowns.objects.filter(fees_distributions_id=FeesDistributions_obj.id,isActive=True)
                            breakdowns_serializers=FeesDistributionsBreakdownsSerializer(get_breakdown_obj,many=True)
                            for b in  breakdowns_serializers.data:
                                alredy_payment_obj=StudentFeesLog.objects.filter(fees_distributions_id=FeesDistributions_obj.id,student_id=student_serializer.data['id'],class_id=class_obj.id,termid=str(b['id'])).first()
                                payment_entry={}
                                payment_entry['fees_distributions_id']=FeesDistributions_obj.id
                                payment_entry['student_id']=student_serializer.data['id']
                                payment_entry['class_id']=class_obj.id
                                payment_entry['termid']=str(b['id'])
                                if alredy_payment_obj is None:
                                    serializer=StudentFeesLogSerializer(data=payment_entry)
                                    if serializer.is_valid():
                                        serializer.save()
                                        successfull_payments.append(payment_entry)
                                    else:
                                        print(serializer.errors)
                                        unsuccessfull_payments.append(payment_entry)


                        else:
                            # want to make make full payment 
                            alredy_payment_obj=StudentFeesLog.objects.filter(fees_distributions_id=FeesDistributions_obj.id,student_id=student_serializer.data['id'],class_id=class_obj.id,termid='').first()
                            payment_entry={}
                            payment_entry['fees_distributions_id']=FeesDistributions_obj.id
                            payment_entry['student_id']=student_serializer.data['id']
                            payment_entry['class_id']=class_obj.id
                            payment_entry['termid']=''
                            if alredy_payment_obj is None:
                                serializer=StudentFeesLogSerializer(data=payment_entry)
                                if serializer.is_valid():
                                    serializer.save()
                                    successfull_payments.append(payment_entry)
                                else:
                                    unsuccessfull_payments.append(payment_entry)
                    else:
                        # want to make make term wise payment 

                        for term in data['termid']:
                            alredy_payment_obj=StudentFeesLog.objects.filter(fees_distributions_id=FeesDistributions_obj.id,student_id=student_serializer.data['id'],class_id=class_obj.id,termid=term).first()
                            payment_entry={}
                            payment_entry['fees_distributions_id']=FeesDistributions_obj.id
                            payment_entry['student_id']=student_serializer.data['id']
                            payment_entry['class_id']=class_obj.id
                            payment_entry['termid']=term
                            if alredy_payment_obj is None:
                                serializer=StudentFeesLogSerializer(data=payment_entry)
                                if serializer.is_valid():
                                    serializer.save()
                                    successfull_payments.append(payment_entry)
                                else:
                                    unsuccessfull_payments.append(payment_entry)

                    if len(unsuccessfull_payments) > 0:
                        return Response({"data":{'unsuccessfull_payments':unsuccessfull_payments,'successfull_payments':successfull_payments},"response": {"n": 0, "msg": "Few fees are not paid","status": "failure"}})
                    
                    else:
                        return Response({"data":{'unsuccessfull_payments':unsuccessfull_payments,'successfull_payments':successfull_payments},"response": {"n": 1, "msg": " Fees  paid successfully","status": "success"}})
                else:
                    return Response({"data":'',"response": {"n": 0, "msg": "Fees not exists","status": "failure"}})     
            else:
                return Response({"data":'',"response": {"n": 0, "msg": "Student class of this class id not found","status": "failure"}})                
        else:
            return Response({"data":'',"response": {"n": 0, "msg": "Student not found","status": "failure"}})



