from User.models import User
from django.core.mail import EmailMessage
from rest_framework.response import Response
from SchoolErp.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password



def createschooladmin(useremail,adminname,schoolcode):
    User.objects.create(
            email=useremail,
            Username = adminname,
            school_code = schoolcode,
            role_id = 2,
            password = str(12345),
            textPassword = str(12345)
        )
    
def send_mail(data, message):
    try:
        msg = EmailMessage(
            data['subject'],
            message,
            EMAIL_HOST_USER,
            [data['email']],
        )
        msg.content_subtype = "html"
        m = msg.send()
        if m:
            print(m)
        data['n'] = 1
        data['Msg'] = 'Email has been sent'
        data['Status'] = "Success"
        return Response(data)
    except Exception as e:
        return Response({'n': 0, 'Msg': 'Email could not be sent', 'Status': 'Failed'})