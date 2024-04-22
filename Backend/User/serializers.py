
from .models import User,MenuItem,permission
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= MenuItem
        fields='__all__'

        

class permissionserializer(serializers.ModelSerializer):
    class Meta:
        model= permission
        fields='__all__'