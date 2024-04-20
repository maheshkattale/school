from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
# Create your views here.
class academic_calender(GenericAPIView):
    def get(self,request):
        return render(request, 'admin/academic_calender/academic_calender.html',{})
    
class get_academic_calender_events(GenericAPIView):
    def post(self,request):
        return Response({"n":0,"status":'success',"data":[]})