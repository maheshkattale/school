from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SubjectMaster.models import Subject
from SchoolMaster.models import AcademicYear

class Days(TrackingModel):
    DayName = models.CharField(max_length=255,null=True,blank=True)  





class TimeTable(TrackingModel):
    AcademicYear = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    ClassId = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    Day = models.CharField(max_length=255,null=True)
    start_time =  models.CharField(max_length=255,null=True)
    end_time = models.CharField(max_length=255,null=True)
    TeacherId =  models.CharField(max_length=250,null=True,blank=True)
    SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
   

