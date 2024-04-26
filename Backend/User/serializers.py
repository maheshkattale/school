
from .models import User,MenuItem,permission,Role
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'

    
class UserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','Username','mobileNumber','email','role','designation','joiningDate','school_code','Address']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= MenuItem
        fields='__all__'

        

class permissionserializer(serializers.ModelSerializer):
    class Meta:
        model= permission
        fields='__all__'
        

class Roleserializer(serializers.ModelSerializer):
    class Meta:
        model= Role
        fields='__all__'