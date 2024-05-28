from .models import *
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from Frontend.school.custom_function import *
class FeesDistributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= FeesDistributions
        fields='__all__'


class StudentFeesLogSerializer(serializers.ModelSerializer):
    class Meta:
        model= StudentFeesLog
        fields='__all__'
        
class FeesDistributionsBreakdownsSerializer(serializers.ModelSerializer):
    class Meta:
        model= FeesDistributionsBreakdowns
        fields='__all__'
class CustomFeesDistributionsSerializer(serializers.ModelSerializer):
    academic_year_id = serializers.StringRelatedField()
    class_id = serializers.StringRelatedField()
    
    academic_year_id_id = serializers.PrimaryKeyRelatedField(source='academic_year_id', queryset=AcademicYear.objects.all())
    class_id_id = serializers.PrimaryKeyRelatedField(source='class_id', queryset=Class.objects.all())
    
    

    


    class Meta:
        model= FeesDistributions
        fields='__all__'
class CustomFeesDistributionsBreakdownsSerializer(serializers.ModelSerializer):
    startdate_dd_mm_yyyy = serializers.SerializerMethodField()
    enddate_dd_mm_yyyy = serializers.SerializerMethodField()
    
    class Meta:
        model= FeesDistributionsBreakdowns
        fields='__all__'
        
    def get_startdate_month_yyyy(self, obj):
        return month_yyyy().to_representation(obj.start_date)

    def get_startdate_dd_mm_yyyy(self, obj):
        return dd_mm_yyyy().to_representation(obj.start_date)

    def get_enddate_month_yyyy(self, obj):
        return month_yyyy().to_representation(obj.end_date)

    def get_enddate_dd_mm_yyyy(self, obj):
        return dd_mm_yyyy().to_representation(obj.end_date)