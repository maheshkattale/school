from django.db import models
from helpers.models import TrackingModel
from User.models import User
from Parent_StudentMaster.models import *

class NotificationTypeMaster(models.Model):
    type_name = models.CharField(max_length=550,null=True,blank=True)   
    def __str__(self):
        return self.type_name


class NotificationMaster(TrackingModel):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='to_user')
    to_user_studentid =  models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True,related_name='to_user_studentid')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='from_user')
    from_user_studentid =  models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True,related_name='from_user_studentid')
    
    notification_title = models.CharField(max_length=51)   
    notification_message= models.CharField(max_length=500, null=True)
    notification_type = models.ForeignKey(NotificationTypeMaster, on_delete=models.CASCADE)
    notification_read = models.BooleanField(default=False)
    school_code = models.CharField(max_length=550,null=True,blank=True)
    
    
