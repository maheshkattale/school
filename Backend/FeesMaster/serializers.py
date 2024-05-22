from .models import *
from rest_framework import serializers

class FeesDistributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= FeesDistributions
        fields='__all__'
        
        
class FeesDistributionsBreakdownsSerializer(serializers.ModelSerializer):
    class Meta:
        model= FeesDistributionsBreakdowns
        fields='__all__'
        
        
        