from .models import Class,ClassTeacher
from rest_framework import serializers
from User.models import User
from SchoolMaster.models import AcademicYear
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model= Class
        fields='__all__'

class ClassTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model= ClassTeacher
        fields='__all__'

class CustomClassTeacherSerializer(serializers.ModelSerializer):

    classid = serializers.StringRelatedField()
    academic_year_id = serializers.StringRelatedField()
    teacherid = serializers.StringRelatedField()
    classid_id = serializers.PrimaryKeyRelatedField(source='classid', queryset=Class.objects.all())
    academic_year_id_id = serializers.PrimaryKeyRelatedField(source='academic_year_id', queryset=AcademicYear.objects.all())
    teacherid_id = serializers.PrimaryKeyRelatedField(source='teacherid', queryset=User.objects.all())

    class Meta:
        model= ClassTeacher
        fields='__all__'