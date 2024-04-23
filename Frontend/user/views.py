from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class profile(GenericAPIView):
    def get(self,request):
        return render(request, 'user/my_profile.html',{})

class reset_password(GenericAPIView):
    def get(self,request):
        return render(request, 'user/reset_password.html',{})
class set_password(GenericAPIView):
    def get(self,request):
        return render(request, 'user/set_password.html',{})