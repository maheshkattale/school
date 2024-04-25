from .models import *
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Students
        fields='__all__'

class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= BloodGroup
        fields='__all__'