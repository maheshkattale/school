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




class CustomExamsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Exams
        fields='__all__'

class CustomExamsSerializer1(serializers.ModelSerializer):
    exam = serializers.StringRelatedField()

    class Meta:
        model= Exams
        fields='__all__'
class ExamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Exam
        fields='__all__'
class ExamTypeMarksSerializer(serializers.ModelSerializer):
    Typeid = serializers.StringRelatedField()
    Type_id = serializers.PrimaryKeyRelatedField(source='Typeid', queryset=ExamType.objects.all())
    

    class Meta:
        model= ExamTypeMarks
        fields='__all__'
        
class ExamTypeMarksSerializer1(serializers.ModelSerializer):

    class Meta:
        model= ExamTypeMarks
        fields='__all__'
        
        
class MarkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model= MarkSheet
        fields='__all__'