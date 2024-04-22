from django.db import models
from helpers.models import TrackingModel

# Create your models here.
class Subject(TrackingModel):
    SubjectName = models.CharField(max_length=255,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
   
    def __str__(self):
        return self.SubjectName
