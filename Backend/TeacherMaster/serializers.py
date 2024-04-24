from .models import TeacherSubject
from rest_framework import serializers

class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= TeacherSubject
        fields='__all__'
        