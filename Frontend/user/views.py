from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.


class profile(GenericAPIView):
    def get(self,request):
        return render(request, 'user/my_profile.html',{})
    