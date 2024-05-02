from django.db import models
from helpers.models import TrackingModel

# Create your models here.
class Class(TrackingModel):
    ClassName = models.CharField(max_length=255,null=True,blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
    def __str__(self):
        return self.ClassName