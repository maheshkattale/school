from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SubjectMaster.models import Subject

class Days(TrackingModel):
    DayName = models.CharField(max_length=255,null=True,blank=True)  



# class TimeTabledaterange(TrackingModel):
    
#     Day = models.ForeignKey(Days,on_delete=models.CASCADE,null=True,blank=True)
#     ClassId = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
#     start_time =  models.CharField(max_length=255,null=True)
#     end_time = models.CharField(max_length=255,null=True)
#     TeacherId =  models.CharField(max_length=250,null=True,blank=True)
#     SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
#     school_code = models.CharField(max_length=150,null=True,blank=True)


class TimeTable(TrackingModel):
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    # daterangeid =  models.ForeignKey(TimeTabledaterange,on_delete=models.CASCADE,null=True,blank=True)
    ClassId = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    # Date = models.DateField(null=True, blank=True)
    Day = models.CharField(max_length=255,null=True)
    # Week = models.CharField(max_length=255,null=True)
    # Month = models.CharField(max_length=255,null=True)
    # Year = models.CharField(max_length=255,null=True)
    start_time =  models.CharField(max_length=255,null=True)
    end_time = models.CharField(max_length=255,null=True)
    TeacherId =  models.CharField(max_length=250,null=True,blank=True)
    SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
   

