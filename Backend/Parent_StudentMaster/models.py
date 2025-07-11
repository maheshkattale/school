from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SchoolMaster.models import AcademicYear

# Create your models here.
class Students(TrackingModel):
    ParentId = models.CharField(max_length=150,null=True,blank=True)
    StudentName = models.TextField(null=True, blank=True)
    StudentCode = models.CharField(max_length=150,null=True,blank=True)
    StudentClass  = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    DateOfBirth =  models.DateField(null=True)
    DateofJoining = models.DateField(null=True)
    BloodGroup = models.IntegerField(null=True,blank=True)
    RollNo = models.CharField(max_length=150,null=True,blank=True)
    photo = models.TextField(null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    primary_student=models.BooleanField(default=False)

    def __str__(self):
        return self.StudentName


class studentclassLog(TrackingModel):
    AcademicyearId = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    studentId =  models.ForeignKey(Students,on_delete=models.CASCADE,null=True,blank=True)
    StudentCode = models.CharField(max_length=150,null=True,blank=True)
    classid = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    RollNo = models.CharField(max_length=150,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    promote_class = models.BooleanField(default=False,null=True,blank=True)


class BloodGroup(TrackingModel):
    Groupname = models.CharField(max_length=200,null=True,blank=True)


class Announcements(TrackingModel):
    Date = models.DateField(null=True)
    AcademicyearId = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    classid = models.JSONField(null=True)
    Announcementtext = models.TextField(null=True,blank=True)
    school_code = models.CharField(max_length=250,null=True,blank=True)
