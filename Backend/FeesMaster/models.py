from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SchoolMaster.models import AcademicYear
from Parent_StudentMaster.models import Students,studentclassLog
from django.utils import timezone

# Create your models here.


class FeesDistributions(TrackingModel):
    total_amount = models.CharField(max_length=150,null=True,blank=True)
    breakdown=models.BooleanField(default=False)
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    academic_year_id = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)

class FeesDistributionsBreakdowns(TrackingModel):
    name = models.CharField(max_length=1150,null=True,blank=True)
    amount = models.CharField(max_length=150,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    fees_distributions_id = models.ForeignKey(FeesDistributions,on_delete=models.CASCADE,null=True,blank=True)



class StudentFeesLog(TrackingModel):
    fees_distributions_id = models.ForeignKey(FeesDistributions,on_delete=models.CASCADE,null=True,blank=True)
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE,null=True,blank=True)
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    Date = models.DateField(default=timezone.now,null=True)
    termid=models.CharField(max_length=150,null=True,blank=True)




















