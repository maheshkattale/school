from django.db import models
from helpers.models import TrackingModel

# Create your models here.
class School(TrackingModel):
    Name = models.CharField(max_length=255,null=True,blank=True)
    Location = models.TextField(null=True,blank=True)
    Contact = models.BigIntegerField(null=True,blank=True)
    Email =  models.EmailField(null=True,blank=True)
    admin_Name = models.CharField(max_length=255,null=True,blank=True)
    admin_Email = models.EmailField(null=True,blank=True)
    school_logo = models.ImageField(upload_to='Schoollogos/', blank=True, null=True,verbose_name='school logo')
    school_code = models.CharField(max_length=255,null=True,blank=True)
   


class AcademicYear(TrackingModel):
    startdate = models.DateField()
    enddate = models.DateField()
    Isdeleted  = models.BooleanField(default=False,blank=True,null=True)
    SchoolId = models.ForeignKey(School,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=255,null=True,blank=True)


