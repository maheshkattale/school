from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SubjectMaster.models import Subject

class Days(TrackingModel):
    DayName = models.CharField(max_length=255,null=True,blank=True)  


class TimeTable(TrackingModel):
    ClassId = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    Date = models.DateField(null=True, blank=True)
    Day = models.ForeignKey(Days,on_delete=models.CASCADE,null=True,blank=True)
    Week = models.CharField(max_length=255,null=True)
    Month = models.CharField(max_length=255,null=True)
    Year = models.CharField(max_length=255,null=True)
    start_time =  models.CharField(max_length=255,null=True)
    end_time = models.CharField(max_length=255,null=True)
    TeacherId =  models.CharField(max_length=250,null=True,blank=True)
    SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
   

