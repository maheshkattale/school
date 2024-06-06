from .models import *
from rest_framework import serializers
from Frontend.school.custom_function import *
class ClassAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= ClassAttendance
        fields='__all__'