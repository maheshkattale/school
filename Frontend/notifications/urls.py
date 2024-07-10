from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('check_new_notification', check_new_notification.as_view(), name = 'check_new_notification'),
    path('check_new_notification_count', check_new_notification_count.as_view(), name = 'check_new_notification_count'),
    path('all_notifications', all_notifications.as_view(), name = 'all_notifications'),

]