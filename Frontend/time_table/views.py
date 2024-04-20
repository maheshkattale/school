from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class time_table_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/time_table_master.html',{})
    
class add_time_table(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/add_time_table.html',{})
    
class edit_time_table(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/time_table_master/edit_time_table.html',{})