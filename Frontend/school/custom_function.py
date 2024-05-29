from django.utils.dateformat import DateFormat
from rest_framework import serializers
from datetime import datetime
import re

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
class serializer_date_yyyy_mm_dd__dd_mm_yyy(serializers.Field):
    def to_representation(self, value):
        date_format = DateFormat(value)
        return date_format.format('d-m-Y')
    
def dd_mm_yyyy_to_yyyy_mm_dd(date_str):
    # Parse the input date string to a datetime object
    if date_str is not None and date_str !="":
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        # Format the datetime object to the desired output format
        new_date_str = date_obj.strftime('%Y-%m-%d')
    else:
        new_date_str=''
        
    return new_date_str

def is_valid_number(number_str):
    if number_str is not None and number_str !='':
        try:
            # Try to convert the string to a float
            float(number_str)
            return True
        except ValueError:
            # If conversion fails, it's not a valid number
            return False
    else:
        return False
        
def starts_with(s,string):
    return s.startswith(string)
    
def is_valid_dd_mm_yyyy(date_str):
    # Define the regular expression pattern for dd-mm-yyyy
    pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$'
    
    # Match the pattern with the input date string
    if re.match(pattern, date_str):
        try:
            # Try to create a datetime object from the input string
            datetime.strptime(date_str, '%d-%m-%Y')
            return True
        except ValueError:
            # If a ValueError is raised, the date is not valid
            return False
    else:
        # If the pattern doesn't match, the date format is not valid
        return False
    
    
    
def is_valid_yyyy_mm_dd(date_str):
    # Define the regular expression pattern for yyyy-mm-dd
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    
    # Match the pattern with the input date string
    if re.match(pattern, date_str):
        try:
            # Try to create a datetime object from the input string
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            # If a ValueError is raised, the date is not valid
            return False
    else:
        # If the pattern doesn't match, the date format is not valid
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    