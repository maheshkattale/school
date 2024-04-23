from django.db import models
from helpers.models import TrackingModel
from SubjectMaster.models import Subject

# Create your models here.
class TeacherSubject(TrackingModel):
    TeacherId = models.CharField(max_length=255,null=True,blank=True)
    SubjectId = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
   
   