from .models import School,AcademicYear
from rest_framework import serializers

class schoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= School
        fields='__all__'


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model= AcademicYear
        fields='__all__'