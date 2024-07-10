from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('check_new_notification', check_new_notification.as_view(), name = 'check_new_notification'),    
    path('mark_read_all_notifications', mark_read_all_notifications.as_view(), name = 'mark_read_all_notifications'),    
    path('check_new_notification_count', check_new_notification_count.as_view(), name = 'check_new_notification_count'),    
    path('user_all_notifications', user_all_notifications.as_view(), name = 'user_all_notifications'),    
]