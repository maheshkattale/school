from django.shortcuts import render
# Create your views here.

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class parent_student_master(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/parent_student_master.html',{})
    
class add_parent_student(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/add_parent_student.html',{})
    
class edit_parent_student(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/parent_student_master/edit_parent_student.html',{})