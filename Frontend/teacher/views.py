from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class teacher_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/teacher_master/teacher_master.html',{})
    
class add_teacher(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/teacher_master/add_teacher.html',{})
    
class edit_teacher(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/teacher_master/edit_teacher.html',{})