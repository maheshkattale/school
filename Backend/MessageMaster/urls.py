from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('add_message', add_message.as_view(), name = 'add_message'),
    path('edit_message', edit_message.as_view(), name = 'edit_message'),
    path('delete_message', delete_message.as_view(), name = 'delete_message'),
    path('get_send_messages', get_send_messages.as_view(), name = 'get_send_messages'),
    path('get_recived_messages', get_recived_messages.as_view(), name = 'get_recived_messages'),
    path('get_recipients', get_recipients.as_view(), name = 'get_recipients'),
    path('check_recipient_type', check_recipient_type.as_view(), name = 'check_recipient_type'),

]