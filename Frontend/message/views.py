from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import json
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from school.static_info import frontend_url
# Create your views here.
send_messages_list_url=frontend_url+'api/MessageMaster/get_send_messages'
recived_messages_list_url=frontend_url+'api/MessageMaster/get_recived_messages'
recipients_list_url=frontend_url+'api/TimeTableMaster/get_recipient'
add_message_url=frontend_url+'api/MessageMaster/add_message'



class messages(GenericAPIView):
    def get(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
                
            data={}    
            if request.session.get('roleid') == 5:
                data['stuid'] = request.session.get('PrimaryStudentId')
                data['StudentCode'] =request.session.get('PrimaryStudentCode')
                
            recipients_list_request = requests.post(recipients_list_url,headers=headers,data=data)
            recipients_list_response = recipients_list_request.json()
                
            send_messages_list_request = requests.post(send_messages_list_url,headers=headers,data=data)
            send_messages_list_response = send_messages_list_request.json()
            recived_messages_list_request = requests.post(recived_messages_list_url,headers=headers,data=data)
            recived_messages_list_response = recived_messages_list_request.json()
            
            return render(request, 'admin/message/messages.html',{
                'recipients':recipients_list_response['data'],
                'send_messages':send_messages_list_response['data'],'recived_messages':recived_messages_list_response['data']})
        else:
            return redirect('school:login')
class add_message(GenericAPIView):
    def post(self,request):
        tok = request.session.get('token', False)
        if tok:
            token = 'Bearer {}'.format(tok)
            headers = {'Authorization':token}
            data = request.data.copy()
            add_message_request = requests.post(add_message_url, data=data,headers=headers)
            add_message_response = add_message_request.json()
            return HttpResponse(json.dumps(add_message_response), content_type="application/json")
        else:
            return redirect('school:login')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        