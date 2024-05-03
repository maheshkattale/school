from .models import *
from rest_framework import serializers

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= ExamType
        fields='__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model= Exams
        fields='__all__'