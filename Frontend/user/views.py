from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
forget_password_url=frontend_url+''

# Create your views here.


class profile(GenericAPIView):
    def get(self,request):
        return render(request, 'user/my_profile.html',{})

class reset_password(GenericAPIView):
    def get(self,request):
        return render(request, 'user/reset_password.html',{})
class forgot_password(GenericAPIView):
    def get(self,request):
        return render(request, 'user/forgot_password.html',{})

    def post(self,request):

        data=request.data.copy()
        forget_password_request = requests.post(forget_password_url,data=data)
        forget_password_response = forget_password_request.json()
        print("forget_password_response",forget_password_response)
        return HttpResponse(json.dumps(forget_password_response), content_type="application/json")

class set_password(GenericAPIView):
    def get(self,request,id):
        return render(request, 'user/set_password.html',{})