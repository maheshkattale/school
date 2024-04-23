from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class class_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/class_master/class_master.html',{})
    
class add_class(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/class_master/add_class.html',{})
    
class edit_class(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/class_master/edit_class.html',{})