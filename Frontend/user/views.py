from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
forget_password_url=frontend_url+'api/User/forgetpasswordmail'
set_password_url=frontend_url+'api/User/setnewpassword'
reset_password_url=frontend_url+'api/User/resetpassword'
# Create your views here.


class profile(GenericAPIView):
    def get(self,request):
        return render(request, 'user/my_profile.html',{})

class reset_password(GenericAPIView):
    def get(self,request,id):
        return render(request, 'user/reset_password.html',{})
    def post(self,request,id):
        data={}
        data['id']=id
        data['cfpassword']=request.POST.get('confirmpassword')
        data['Password']=request.POST.get('newpassword')
        
        reset_password_request = requests.post(reset_password_url,data=data)
        reset_password_response = reset_password_request.json()
        print("reset_password_response['response']['n']",reset_password_response)
        if reset_password_response['response']['n']==0:
            msg = reset_password_response['response']['msg']
            messages.error(request, msg)
            return render(request, 'user/reset_password.html',{})
        else:
            msg = reset_password_response['response']['msg']
            messages.success(request, msg)
            return redirect('school:login')
        
        
        
class forgot_password(GenericAPIView):
    def get(self,request):
        return render(request, 'user/forgot_password.html',{})

    def post(self,request):

        data=request.data.copy()
        forget_password_request = requests.post(forget_password_url,data=data)
        forget_password_response = forget_password_request.json()
        
        
        if forget_password_response['response']['n']==0:
            msg = forget_password_response['response']['msg']
            messages.error(request, msg)
            return redirect('user:forgot_password')
        
        else:
 
            msg = forget_password_response['response']['msg']
            messages.success(request, msg)
            return redirect('school:login')
            

class set_password(GenericAPIView):
    def get(self,request,id):
        print("id",id)
        return render(request, 'user/set_password.html',{})
    def post(self,request,id):
        data={}
        data['id']=id
        data['cfpassword']=request.POST.get('confirmpassword')
        data['Password']=request.POST.get('newpassword')
        
        set_password_request = requests.post(set_password_url,data=data)
        set_password_response = set_password_request.json()
        print("set_password_response['response']['n']",set_password_response)
        if set_password_response['response']['n']==0:
            msg = set_password_response['response']['msg']
            messages.error(request, msg)
            return render(request, 'user/set_password.html',{})
        
        else:
 
            msg = set_password_response['response']['msg']
            messages.success(request, msg)
            return redirect('school:login')
        