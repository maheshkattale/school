from .models import *
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from Frontend.school.custom_function import *


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model= Messages
        fields='__all__'
        

class CustomMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model= Messages
        fields='__all__'
