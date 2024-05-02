from .models import *
from User.models import *
from rest_framework import serializers
from django.utils.dateformat import DateFormat
class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model= TimeTable
        fields='__all__'
class CustomDateFormatField(serializers.Field):
    def to_representation(self, value):
        date_format = DateFormat(value)
        return date_format.format('d F Y')

class CustomTimeTableSerializer(serializers.ModelSerializer):
    ClassId = serializers.StringRelatedField()
    SubjectId = serializers.StringRelatedField()
    enddate = CustomDateFormatField()
    startdate = CustomDateFormatField()
    teacher_name = serializers.SerializerMethodField()
    # Assuming other fields follow the existing structure

    def get_teacher_name(self, obj):
        teacher_id = obj.TeacherId
        if teacher_id:
            try:
                teacher = User.objects.get(id=teacher_id)
                return teacher.Username
            except User.DoesNotExist:
                return None
        return None


    class Meta:
        model= TimeTable
        fields='__all__'