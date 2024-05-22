from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
forget_password_url=frontend_url+'api/User/forgetpasswordmail'

# Create your views here.


class fees_distrubution(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/fees_master/fees_distribution.html',{})