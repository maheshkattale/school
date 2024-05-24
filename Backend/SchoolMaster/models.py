from django.db import models
from helpers.models import TrackingModel
from ClassMaster.models import Class
# Create your models here.
class School(TrackingModel):
    Name = models.CharField(max_length=255,null=True,blank=True)
    Location = models.TextField(null=True,blank=True)
    Contact = models.BigIntegerField(null=True,blank=True)
    Email =  models.EmailField(null=True,blank=True)
    admin_Name = models.CharField(max_length=255,null=True,blank=True)
    admin_Email = models.EmailField(null=True,blank=True)
    school_logo = models.ImageField(upload_to='Schoollogos/', blank=True, null=True,verbose_name='school logo')
    school_code = models.CharField(max_length=255,null=True,blank=True)
   


class AcademicYear(TrackingModel):
    startdate = models.DateField()
    enddate = models.DateField()
    Isdeleted  = models.BooleanField(default=False,blank=True,null=True)
    SchoolId = models.ForeignKey(School,on_delete=models.CASCADE,null=True,blank=True)
    school_code = models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        ordering = ['-startdate']
        indexes = [
            models.Index(fields=['startdate', 'enddate']),
        ]
    
    def __str__(self):
        return f"{self.format_date(self.startdate)} to {self.format_date(self.enddate)}"

    def format_date(self, date):
        return date.strftime('%d') + self.day_suffix(date.day) + ' ' + date.strftime('%B %Y')

    def day_suffix(self, day):
        if 11 <= day <= 13:
            return 'th'
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')  

