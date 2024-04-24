from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
# Create your views here.
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .static_info import frontend_url
# Create your views here.
login_url=frontend_url+"api/User/login"
logout_url = frontend_url+'api/User/logout'

class login(GenericAPIView):
    def get(self,request):
        return render(request, 'login.html',{})
    def post(self,request):
        print("hiiiii")
        email = request.POST['email']
        password = request.POST['password']
        source = request.POST['source']
        data = {}
        data['email'] = email
        data['password'] = password
        data['source'] = source
        
        
        login_request = requests.post(login_url, data=data)
        login_response = login_request.json()
        print("login_response",login_response)
        if login_response['response']['n']==0:
            msg = login_response['response']['msg']
            messages.error(request, msg)
            return redirect('school:login')
        
        else:
            request.session['token'] = login_response['data']['token']
            request.session['schoolcode'] = login_response['data']['schoolcode']
            request.session['username'] = login_response['data']['username']
            msg = login_response['response']['msg']
            messages.success(request, msg)
            return redirect('school:dashboard')


class logout(GenericAPIView):
    def get(self,request):
        try:
            tok = request.session.get('token', False)
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            logout_request = requests.post(logout_url, headers=headers)
            logout_response = logout_request.json()
            if logout_response['response']['n'] == 1:
                del request.session['token']
                messages.success(request, logout_response['response']['msg'])
                return redirect('school:login')
            else:
                messages.error(request, logout_response['response']['msg'])
                return redirect('school:login')
        except Exception as e:
            messages.error(request, e)
            return redirect('school:login')




class dashboard(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            return render(request, 'admin/dashboard.html',{})

        messages.error(request, 'Session expired please login again')
        return redirect('school:login')
    

    
    
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