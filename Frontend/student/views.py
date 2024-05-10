from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
from django.contrib import messages
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
student_list_url=frontend_url+''


class student_list(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # student_list_request = requests.get(student_list_url,headers=headers)
            # student_list_response = student_list_request.json()
            # if student_list_response['response']['n']==1:
            #     return render(request, 'admin/student_master/student_master.html',{'students':student_list_response['data']})
            # else:
            #     messages.error(request, student_list_response['response']['msg'])
            #     return redirect('school:login') 
            
            return render(request, 'admin/student_master/studentlist.html',{'students':[]})

        else:
            return redirect('school:login')
        
        
class student_id_cards(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            # student_list_request = requests.get(student_list_url,headers=headers)
            # student_list_response = student_list_request.json()
            # if student_list_response['response']['n']==1:
            #     return render(request, 'admin/student_master/student_master.html',{'students':student_list_response['data']})
            # else:
            #     messages.error(request, student_list_response['response']['msg'])
            #     return redirect('school:login') 
            
            return render(request, 'admin/student_master/studentcards.html',{'students':[]})

        else:
            # messages.error(request, student_list_response['response']['msg'])
            return redirect('school:login')