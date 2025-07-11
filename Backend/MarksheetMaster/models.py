from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
from SubjectMaster.models import Subject
from Parent_StudentMaster.models import Students
from SchoolMaster.models import AcademicYear

# Create your models here.


class ExamType(TrackingModel):
    TypeName = models.CharField(max_length=150,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    def __str__(self):
        return self.TypeName



class ExamTypeMarks(TrackingModel):
    Typeid = models.ForeignKey(ExamType,on_delete=models.CASCADE,null=True,blank=True)
    Marks =  models.CharField(max_length=150,null=True,blank=True)
    passingmarks =  models.CharField(max_length=150,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)


class Exam(TrackingModel):
    Name =  models.CharField(max_length=550,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    def __str__(self):
        return self.Name



class Exams(TrackingModel):    #Schedule
    ClassId = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    Date = models.DateField(null=True,blank=True)
    Examstarttime = models.CharField(max_length=255,null=True,blank=True)
    Examendtime = models.CharField(max_length=255,null=True,blank=True)
    InvigilatorId =  models.CharField(max_length=250,null=True,blank=True)   #user table
    SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    ExamType =  models.ForeignKey(ExamType,on_delete=models.CASCADE,null=True,blank=True)  #paper type
    totalMarks = models.CharField(max_length=255,null=True,blank=True)
    passingmarks = models.CharField(max_length=255,null=True,blank=True)  #not in excel

    reportTime =  models.CharField(max_length=255,null=True,blank=True)
    RoomNo = models.CharField(max_length=255,null=True,blank=True)
    Instructions = models.TextField(null=True,blank=True)
    AcademicYearId = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True,blank=True)  #exam name
    school_code = models.CharField(max_length=150,null=True,blank=True)


class MarkSheet(TrackingModel):
    AcademicYearId = models.BigIntegerField(null=True,blank=True)
    ClassId = models.BigIntegerField(null=True,blank=True)
    StudentId=  models.BigIntegerField(null=True,blank=True)
    subID =  models.CharField(max_length=255,null=True,blank=True)  
    ObtainedMarks =  models.CharField(max_length=255,null=True,blank=True)
    OutOfMarks =  models.FloatField(null=True,blank=True)
    Status = models.CharField(max_length=150,null=True,blank=True)
    Exam=models.BigIntegerField(null=True,blank=True)
    RollNo = models.CharField(max_length=150,null=True,blank=True) #
    school_code = models.CharField(max_length=150,null=True,blank=True)



