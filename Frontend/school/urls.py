from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', login.as_view(), name = 'login'),
    path('logout', logout.as_view(), name = 'logout'),
    path('login', login.as_view(), name = 'login_page'),
    path('dashboard', dashboard.as_view(), name = 'dashboard'),
    path('school_master', school_master.as_view(), name = 'school_master'),
    path('add_school', add_school.as_view(), name = 'add_school'),
    path('edit_school', edit_school.as_view(), name = 'edit_school'),
    path('mail', mail.as_view(), name = 'mail'),
    path('marksheet', marksheet.as_view(), name = 'marksheet'),
    path('permissions', permissions.as_view(), name = 'permissions'),
    path('reset_password_mail', reset_password_mail.as_view(), name = 'reset_password_mail'),

    
]