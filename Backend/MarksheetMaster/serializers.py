from .models import *
from rest_framework import serializers
from Frontend.school.custom_function import *
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
    AcademicYearId = serializers.StringRelatedField()
    AcademicYearId_id = serializers.PrimaryKeyRelatedField(source='AcademicYearId', queryset=AcademicYear.objects.all())
    exam_id = serializers.PrimaryKeyRelatedField(source='exam', queryset=Exam.objects.all())
    exam = serializers.StringRelatedField()
    ClassId_id = serializers.PrimaryKeyRelatedField(source='ClassId', queryset=Class.objects.all())
    ClassId = serializers.StringRelatedField()


    class Meta:
        model= Exams
        fields=['AcademicYearId','AcademicYearId_id','exam','exam_id','ClassId','ClassId_id']



class CustomExamsSerializer2(serializers.ModelSerializer):
    ExamType = serializers.StringRelatedField()
    SubjectId = serializers.StringRelatedField()
    ClassId = serializers.StringRelatedField()
    Date = CustomDateFormatField()

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