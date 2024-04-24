from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
class_list_url=frontend_url+'api/ClassMaster/List'

class class_master(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            class_list_request = requests.get(class_list_url,headers=headers)
            class_list_response = class_list_request.json()
            print("class_list_response",class_list_response)
            if class_list_response['response']['n']==1:
                return render(request, 'admin/class_master/class_master.html',{'classes':class_list_response['data']})
            else:
                messages.error(request, class_list_response['response']['msg'])
                return redirect('school:login') 
        else:
            messages.error(request, class_list_response['response']['msg'])
            return redirect('school:login')
        
class add_class(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/class_master/add_class.html',{})
    
class edit_class(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/class_master/edit_class.html',{})