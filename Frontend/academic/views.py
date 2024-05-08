from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
add_academic_dates_url=frontend_url+''

class academic_master(GenericAPIView):
    def get(self,request):
        print("id",id)
        return render(request, 'admin/academic/academic_master.html',{})
    
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            print("data",data)
            add_academic_dates_request = requests.post(add_academic_dates_url,data=data,headers=headers)
            add_academic_dates_response = add_academic_dates_request.json()
            return HttpResponse(json.dumps(add_academic_dates_response), content_type="application/json")
        else:
            return redirect('school:login')
        