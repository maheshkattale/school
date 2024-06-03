from django.db import models
from helpers.models import TrackingModel
from User.models import User
from SchoolMaster.models import AcademicYear


# Create your models here.
class Class(TrackingModel):
    ClassName = models.CharField(max_length=255,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    def __str__(self):
        return self.ClassName
    
class ClassTeacher(TrackingModel):
    classid =models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    teacherid =models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    academic_year_id =models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)


