from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login.as_view(), name = 'login'),
    path('logout', logout.as_view(), name = 'logout'),
    path('userlist', Userlist.as_view(), name = 'Userlist'),
    path('getpermissions', getpermissions.as_view(), name = 'getpermissions'),
    path('savepermissions', savepermissions.as_view(), name = 'savepermissions'),
    path('changepassword', ChangePassword.as_view(), name = 'changepassword'),
    path('forgetpasswordmail', forgetpasswordmail.as_view(), name = 'forgetpasswordmail'),
    path('setnewpassword', setnewpassword.as_view(), name = 'setnewpassword'),
    path('resetpassword', resetpassword.as_view(), name = 'resetpassword'),
    path('menuitems', Menulist.as_view(), name = 'menuitems'),
    path('getrole', getrole.as_view(), name = 'getrole'),
    path('update_profile', update_profile.as_view(), name = 'update_profile'),

    #Announcements
    
    
    
]