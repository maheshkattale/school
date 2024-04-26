from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from helpers.models import TrackingModel
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid
import jwt
from datetime import datetime, timedelta
from DesignationMaster.models import Designation
from django.db.models.deletion import CASCADE

# Create your models here.

class Role(TrackingModel):
    RoleName = models.CharField(max_length=150)
   
    def __str__(self):
        return self.RoleName


class MenuItem(models.Model):
    MenuID = models.IntegerField(primary_key=True)
    MenuName = models.CharField(max_length=50)
    MenuPath = models.CharField(max_length=50, null=True, blank=True)
    MenuIcon = models.CharField(max_length=50, null=True, blank=True)
    ParentID =  models.IntegerField(null=True, blank=True)
    SortOrder = models.IntegerField(null=True, blank=True)
    school_code = models.CharField(max_length=100,null=True, blank=True)

   
class permission(TrackingModel):
    Role_id = models.ForeignKey(Role , on_delete=models.CASCADE,null=True)
    permission = models.ManyToManyField(MenuItem)
    school_code = models.CharField(max_length=100,null=True, blank=True)


class UserManager(BaseUserManager):
    def create(self,email,password,**extra_fields):
        if not email:
            raise ValueError("User must have a valid email")
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,TrackingModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Username = models.CharField(max_length=255,null=True,blank=True)
    textPassword = models.CharField(max_length=255,null=True,blank=True)
    mobileNumber = models.BigIntegerField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
    designation = models.ForeignKey(Designation,on_delete=models.CASCADE,null=True,blank=True)
    joiningDate = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=255,null=True,blank=True)
    school_code = models.CharField(max_length=100,null=True, blank=True)
    PasswordSet = models.BooleanField(default=False)
    Address = models.TextField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserToken(TrackingModel):
    User = models.CharField(max_length=255,null=True, blank=True)
    source = models.CharField(max_length=255,null=True,blank=True)
    WebToken = models.TextField(null=True, blank=True)
    MobileToken = models.TextField(null=True, blank=True)




