from .models import School
from rest_framework import serializers

class schoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= School
        fields='__all__'