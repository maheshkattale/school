from .models import *
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Students
        fields='__all__'