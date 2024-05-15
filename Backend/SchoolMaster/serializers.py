from .models import School,AcademicYear
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from Frontend.school.custom_function import *
class schoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= School
        fields='__all__'



    
    
class AcademicYearSerializer1(serializers.ModelSerializer):
    startdate_month_yyyy = serializers.SerializerMethodField()
    startdate_dd_mm_yyyy = serializers.SerializerMethodField()
    enddate_month_yyyy = serializers.SerializerMethodField()
    enddate_dd_mm_yyyy = serializers.SerializerMethodField()
    

    class Meta:
        model= AcademicYear
        fields='__all__'
    def get_startdate_month_yyyy(self, obj):
        return month_yyyy().to_representation(obj.startdate)

    def get_startdate_dd_mm_yyyy(self, obj):
        return dd_mm_yyyy().to_representation(obj.startdate)

    def get_enddate_month_yyyy(self, obj):
        return month_yyyy().to_representation(obj.enddate)

    def get_enddate_dd_mm_yyyy(self, obj):
        return dd_mm_yyyy().to_representation(obj.enddate)
        
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model= AcademicYear
        fields='__all__'