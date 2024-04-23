from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .static_info import frontend_url
# Create your views here.

class login(GenericAPIView):
    def get(self,request):
        return render(request, 'login.html',{})

class dashboard(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/dashboard.html',{})
    

    
    
class school_master(GenericAPIView):
    def get(self,request):
        return render(request, 'superadmin/school_master.html',{})
    
    
class add_school(GenericAPIView):
    def get(self,request):
        return render(request, 'superadmin/add_school.html',{})
    
class edit_school(GenericAPIView):
    def get(self,request):
        return render(request, 'superadmin/edit_school.html',{})
class mail(GenericAPIView):
    def get(self,request):
        return render(request, 'mails/school_registration.html',{'Admin_Name':'Mahesh Kattale','frontend_url':frontend_url})
    
class reset_password_mail(GenericAPIView):
    def get(self,request):
        return render(request, 'mails/reset_password.html',{'Admin_Name':'Mahesh Kattale','frontend_url':frontend_url})
class marksheet(GenericAPIView):
    def get(self,request):
        return render(request, 'commingsoon.html',{})
    

class permissions(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/permissions.html',{})