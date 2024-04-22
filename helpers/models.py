from django.db import models

class TrackingModel(models.Model):
    createdAt=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updatedAt=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    createdBy=models.CharField(max_length=255,null=True, blank=True)
    updatedBy=models.CharField(max_length=255,null=True, blank=True)
    isActive=models.BooleanField(default=True,blank=True,null=True)
    class Meta:
        abstract=True
        ordering=('-createdAt',)