from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView





class Adduser(GenericAPIView):
    def post(self,request):
       
        return Response({"data":'',"response": {"n": 1, "msg": "Company added successfully","status": "success"}})
           
