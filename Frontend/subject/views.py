from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class subject_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/subject_master/subject_master.html',{})
    
class add_subject(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/subject_master/add_subject.html',{})
    
class edit_subject(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/subject_master/edit_subject.html',{})