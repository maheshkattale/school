from django.utils.dateformat import DateFormat
from rest_framework import serializers
from datetime import datetime
import re
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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
    
    
    
def calculate_percentage(obtained_marks, total_marks):
    """
    Calculate the percentage of obtained marks out of total marks.

    Parameters:
    obtained_marks (float or int): The marks obtained.
    total_marks (float or int): The total marks.

    Returns:
    float: The percentage of obtained marks out of total marks.
    """
    if total_marks == 0:
        return 0

    percentage = round((obtained_marks / total_marks) * 100)
    return percentage
    
    
def get_day_name(date_str):
    # Convert the string to a date object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    # Get the day name
    day_name = date_obj.strftime('%A')
    return day_name
    
    
    
    
def validate_start_date_and_end_date(start_date_str, end_date_str):
    date_format = "%Y-%m-%d"
    try:
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
    except ValueError:
        return {"status":True,"Reason":"Incorrect date format, should be YYYY-MM-DD"}
    
    if start_date > end_date:
        return {"status":True,"Reason":'Start date should be before end date'}
    
    return {"status":False,"Reason":'valid date'}
    
def validate_day_name(day_name):
    
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if day_name.capitalize() in valid_days:
        return True
    else:
        return False
def validate_start_time_and_end_time(start_time_str, end_time_str):
    time_format = "%H:%M"
    try:
        start_time = datetime.strptime(start_time_str, time_format).time()
        end_time = datetime.strptime(end_time_str, time_format).time()
    except ValueError:
        return {"status": True, "Reason": "Incorrect time format, should be HH:MM"}
    
    if start_time >= end_time:
        return {"status": True, "Reason": "Start time should be before end time"}
    
    return {"status": False, "Reason": "Valid times"}
    
    

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self,data):
        response = Response({
            'data':data,
            'response':{
                'n':1,
                'status':"success",
                'count':self.page.paginator.count,
                'next' : self.get_next_link(),
                'previous' : self.get_previous_link(),
            }
        })
        return response    
    
    
    