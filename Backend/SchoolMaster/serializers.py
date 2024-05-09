from .models import School,AcademicYear
from rest_framework import serializers
from django.utils.dateformat import DateFormat

class schoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= School
        fields='__all__'


class CustomDateFormatField(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%d-%m-%Y')
    
    
class AcademicYearSerializer1(serializers.ModelSerializer):
    startdate = CustomDateFormatField()
    enddate = CustomDateFormatField()

    class Meta:
        model= AcademicYear
        fields='__all__'
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model= AcademicYear
        fields='__all__'