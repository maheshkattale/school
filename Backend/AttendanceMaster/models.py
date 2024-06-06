from django.db import models
from helpers.models import TrackingModel
from User.models import User
from SchoolMaster.models import AcademicYear
from ClassMaster.models import Class
from Parent_StudentMaster.models import Students

# Create your models here.
class ClassAttendance(TrackingModel):
    class_id =models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
    academic_year_id =models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    Date = models.DateField(null=True,blank=True)
    student_id =models.ForeignKey(Students,on_delete=models.CASCADE,null=True,blank=True)
    IsPresent=models.BooleanField(default=False,null=True,blank=True)
