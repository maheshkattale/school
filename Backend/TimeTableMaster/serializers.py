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

    def get_teacher_name(self, obj):
        teacher_id = obj.TeacherId
        if teacher_id:
            try:
                teacher = User.objects.get(id=teacher_id)
                return teacher.Username
            except User.DoesNotExist:
                return None
        return None
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['start_time'] = self.format_time(instance.start_time) if instance.start_time else None
        representation['end_time'] = self.format_time(instance.end_time) if instance.end_time else None
        return representation
    
    def format_time(self, time_str):
        if time_str:
            time_obj = datetime.strptime(time_str, '%H:%M')
            return time_obj.strftime('%I:%M %p')
        return None

    class Meta:
        model= TimeTable
        fields='__all__'