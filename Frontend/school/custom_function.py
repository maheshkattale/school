from django.utils.dateformat import DateFormat
from rest_framework import serializers

class dd_mm_yyyy(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%d-%m-%Y')
    
    
class month_yyyy(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%B %Y')
    
class dd_month_yyyy(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%d %B %Y')
class CustomDateFormatField(serializers.Field):
    def to_representation(self, value):
        date_format = DateFormat(value)
        return date_format.format('d F Y')
    
    
    
    
    
    
    
    
    
    
    
    
    