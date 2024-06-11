from .models import *
from User.models import *
from rest_framework import serializers
from Frontend.school.custom_function import *
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Students
        fields='__all__'

class custom_student_serializer_id_list(serializers.ListSerializer):
    def to_representation(self, data):
        return [item.id for item in data]

class custom_student_serializer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = ['id']
        list_serializer_class = custom_student_serializer_id_list


class custom_student_classlog_serializer_studentid_list(serializers.ListSerializer):
    def to_representation(self, data):
        return [item.studentId for item in data]

class custom_studentid_classlog_serializer(serializers.ModelSerializer):

    class Meta:
        model = studentclassLog
        fields = ['studentId']
        list_serializer_class = custom_student_classlog_serializer_studentid_list

class StudentSerializer1(serializers.ModelSerializer):
    StudentClass=serializers.StringRelatedField()
    class Meta:
        model= Students
        fields='__all__'

class StudentSerializer2(serializers.ModelSerializer):
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

class custom_studentclassLogserializer(serializers.ModelSerializer):
    studentId=serializers.StringRelatedField()
    classid=serializers.StringRelatedField()
    studentId_id = serializers.PrimaryKeyRelatedField(source='studentId', queryset=Students.objects.all())
    classid_id = serializers.PrimaryKeyRelatedField(source='classid', queryset=Class.objects.all())

    class Meta:
        model= studentclassLog
        fields='__all__'

class custom_student_class_log_serializer_class_id_list(serializers.ListSerializer):
    def to_representation(self, data):
        return [item.classid for item in data]

class custom_student_class_log_serializer(serializers.ModelSerializer):
    classid = serializers.PrimaryKeyRelatedField(source='classid', queryset=Class.objects.all())

    class Meta:
        model = studentclassLog
        fields = ['classid']
        list_serializer_class = custom_student_class_log_serializer_class_id_list
        
        

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model= Announcements
        fields='__all__'
class CustomAnnouncementSerializer(serializers.ModelSerializer):
    Date = CustomDateFormatField()
    AcademicyearId = serializers.StringRelatedField()
    classes_names = serializers.SerializerMethodField()

    def get_classes_names(self, obj):
        class_id_list=obj.classid
        if len(class_id_list) >0:
            try:
                classes_names=[]
                for i in class_id_list:
                    class_obj = Class.objects.get(id=i)
                    classes_names.append(class_obj.ClassName)
                        
                return classes_names
            except Exception as e:
                return e
        return []
    class Meta:
        model= Announcements
        fields='__all__'
        
class CustomAnnouncementSerializer2(serializers.ModelSerializer):
    Date = CustomDateFormatField()
    class Meta:
        model= Announcements
        fields='__all__'

        

class CustomStudentSerializer(serializers.ModelSerializer):
    StudentClass=serializers.StringRelatedField()
    DateOfBirth = CustomDateFormatField()
    DateofJoining = CustomDateFormatField()

    bloodgroup_name = serializers.SerializerMethodField()

    def get_bloodgroup_name(self, obj):
        bloodgroup_id = obj.BloodGroup
        if bloodgroup_id:
            try:
                bloodgroup = BloodGroup.objects.get(id=bloodgroup_id)
                return bloodgroup.Groupname
            except BloodGroup.DoesNotExist:
                return None
        return None


    class Meta:
        model= Students
        fields='__all__'
        
        
        
        
