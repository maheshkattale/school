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
change_password_url=frontend_url+'api/User/changepassword'
    
permission_url=frontend_url+'api/User/getpermissions'
menuitems_url=frontend_url+'api/User/menuitems'
role_url=frontend_url+'api/User/getrole'
save_permissions_url=frontend_url+'api/User/savepermissions'
update_profile_url=frontend_url+'api/User/update_profile'
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
class change_password(GenericAPIView):
    
    def get(self,request,id):
        return render(request, 'user/change_password.html',{})

    def post(self,request,id):
        
        tok = request.session.get('token', False)
        if tok:
            
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            data['id']=id
            data['newpassword']=request.POST.get('newpassword')
            data['confirmpassword']=request.POST.get('confirmpassword')
            data['oldpassword']=request.POST.get('oldpassword')
            change_password_request = requests.post(change_password_url,data=data,headers=headers)
            change_password_response = change_password_request.json()
            
            
            if change_password_response['response']['n']==0:
                msg = change_password_response['response']['msg']
                messages.error(request, msg)
                return redirect('school:dashboard')
            
            else:
                msg = change_password_response['response']['msg']
                messages.success(request, msg)
                return redirect('school:login')
class set_password(GenericAPIView):
    def get(self,request,id):
        return render(request, 'user/set_password.html',{})
    def post(self,request,id):
        data={}
        data['id']=id
        data['cfpassword']=request.POST.get('confirmpassword')
        data['Password']=request.POST.get('newpassword')
        
        set_password_request = requests.post(set_password_url,data=data)
        set_password_response = set_password_request.json()
        if set_password_response['response']['n']==0:
            msg = set_password_response['response']['msg']
            messages.error(request, msg)
            return render(request, 'user/set_password.html',{})
        
        else:
 
            msg = set_password_response['response']['msg']
            messages.success(request, msg)
            return redirect('school:login')    
           
class permissions(GenericAPIView):
    def get(self,request):

        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}


            menuitems_request = requests.get(menuitems_url,headers=headers)
            menuitems_response = menuitems_request.json()

            role_request = requests.get(role_url,headers=headers)
            role_response = role_request.json()

            context={
                'menuitems':menuitems_response['data'],
                'roles':role_response['data'],
            }
            return render(request, 'user/permissions.html',context)
        else:
            return redirect('school:login')
        
    def post(self,request):

        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            data['roleid'] = request.data.get('roleid')
            data['permission'] = request.data.getlist('permission')            
            save_permissions_request = requests.post(save_permissions_url,headers=headers,data=data)
            save_permissions_response = save_permissions_request.json()
            if save_permissions_response['response']['n']==1:
                messages.success(request, save_permissions_response['response']['msg'])
            else:
                messages.error(request, save_permissions_response['response']['msg'])
                

            return redirect('user:permissions')
        else:
            return redirect('user:permissions')
class get_permissions_by_role(GenericAPIView):
    def post(self,request):

        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data={}
            data['roleid']=request.POST.get("roleid")
            permission_request = requests.get(permission_url,headers=headers,data=data)
            permission_response = permission_request.json()
            return HttpResponse(json.dumps(permission_response), content_type="application/json")

        else:
            return redirect('school:login')
        
  
  
  
class update_profile(GenericAPIView):
    def post(self,request):

        tok = request.session.get('token', False)
        if tok:
            t = 'Token {}'.format(tok)
            headers = {'Authorization': t}
            data=request.data.copy()
            update_profile_request = requests.get(update_profile_url,headers=headers,data=data,files=request.FILES)
            update_profile_response = update_profile_request.json()
            print("update_profile_response",update_profile_response)
            if update_profile_response['response']['n']==1:
                request.session['profile_image'] = update_profile_response['data']['photo']
                request.session['mobileNumber'] = update_profile_response['data']['mobileNumber']
                request.session['Address'] = update_profile_response['data']['Address']

            return HttpResponse(json.dumps(update_profile_response), content_type="application/json")