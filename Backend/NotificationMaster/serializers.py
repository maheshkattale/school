from .models import *
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from Frontend.school.custom_function import *
from User.models import *

class NotificationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model= NotificationMaster
        fields='__all__'
class CustomNotificationMasterSerializer(serializers.ModelSerializer):
    createdAt=CustomDateFormatField()
    notification_type=serializers.StringRelatedField()
    from_user = serializers.StringRelatedField()
    from_user_id = serializers.PrimaryKeyRelatedField(source='from_user', queryset=User.objects.all())
    from_user_name = serializers.SerializerMethodField()

    class Meta:
        model= NotificationMaster
        fields='__all__'
    def get_from_user_name(self, obj):
        return obj.from_user.Username if obj.from_user else None