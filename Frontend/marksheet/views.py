from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
generate_marksheet_url=frontend_url+'api/MarksheetMaster/GenerateMarkSheet'




class generate_marksheet(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data=request.data.copy()
            generate_marksheet_request = requests.post(generate_marksheet_url,headers=headers,data=data)
            generate_marksheet_response = generate_marksheet_request.json()
            return HttpResponse(json.dumps(generate_marksheet_response), content_type="application/json")
        else:
            return redirect('school:login')