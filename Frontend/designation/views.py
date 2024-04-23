from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class designation_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/designation_master/designation_master.html',{})
    
class add_designation(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/designation_master/add_designation.html',{})
    
class edit_designation(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/designation_master/edit_designation.html',{})