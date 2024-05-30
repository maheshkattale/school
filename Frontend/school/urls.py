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
    path('edit_school/<str:id>', edit_school.as_view(), name = 'edit_school'),
    path('disable_school', disable_school.as_view(), name = 'disable_school'),
    path('enable_school', enable_school.as_view(), name = 'enable_school'),
    path('mail', mail.as_view(), name = 'mail'),
    path('template_render', template_render.as_view(), name = 'template_render'),
    path('promote_marksheet', promote_marksheet.as_view(), name = 'promote_marksheet'),
    path('generate_marksheet', generate_marksheet.as_view(), name = 'generate_marksheet'),
    path('upload_marksheet', upload_marksheet.as_view(), name = 'upload_marksheet'),
    path('permissions', permissions.as_view(), name = 'permissions'),
    path('reset_password_mail', reset_password_mail.as_view(), name = 'reset_password_mail'),

    
]
