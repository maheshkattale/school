from .models import *
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Students
        fields='__all__'

class StudentSerializer1(serializers.ModelSerializer):
    StudentClass=serializers.StringRelatedField()
    class Meta:
        model= Students
        fields='__all__'

class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= BloodGroup
        fields='__all__'


class studentclassLogserializer(serializers.ModelSerializer):
    class Meta:
        model= studentclassLog
        fields='__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model= Announcements
        fields='__all__'