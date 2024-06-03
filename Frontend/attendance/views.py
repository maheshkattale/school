from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
forget_password_url=frontend_url+'api/User/forgetpasswordmail'
academic_list_url=frontend_url+'api/SchoolMaster/AcademicYearlist'

# Create your views here.

class class_attendance(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # fees_destributiom_list_request = requests.get(fees_destributiom_list_url,headers=headers)
            # fees_destributiom_list_response = fees_destributiom_list_request.json()
            return render(request, 'admin/fees_master/fees_distribution.html',{'fees':fees_destributiom_list_response['data']})
        else:
            return redirect('school:login')