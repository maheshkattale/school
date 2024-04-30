from .models import *
from rest_framework import serializers

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model= TimeTable
        fields='__all__'