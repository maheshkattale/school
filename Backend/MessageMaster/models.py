from django.db import models
from helpers.models import TrackingModel

# Create your models here.
class Messages(TrackingModel):
    from_user_id = models.CharField(max_length=150,null=True,blank=True)
    from_user_str = models.CharField(max_length=500, null=True)
    from_user_studentcode = models.CharField(max_length=150,null=True,blank=True)
    
    message = models.TextField()
    short_message = models.TextField()
    to_user_id =models.CharField(max_length=150)
    to_user_str = models.CharField(max_length=500)
    
    to_user_studentcode = models.CharField(max_length=150,null=True,blank=True)
    

    date_str = models.DateField(null=True, blank=True)
    school_code = models.CharField(max_length=150,null=True,blank=True)
