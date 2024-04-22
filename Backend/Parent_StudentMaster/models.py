from django.db import models
from helpers.models import TrackingModel


# Create your models here.
class Students(TrackingModel):
    ParentId = models.IntegerField(null=True,blank=True)
    StudentName = models.TextField(null=True, blank=True)
    StudentCode = models.CharField(max_length=150,null=True,blank=True)
    StudentClass = models.CharField(max_length=150,null=True,blank=True)
    DateOfBirth =  models.DateField(null=True)
    DateofJoining = models.DateField(null=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)

   