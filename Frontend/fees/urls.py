from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('fees_distrubution', fees_distrubution.as_view(), name = 'fees_distrubution'),
    path('add_fees_distrubution', add_fees_distrubution.as_view(), name = 'add_fees_distrubution'),
    path('delete_fees', delete_fees.as_view(), name = 'delete_fees'),
    path('edit_fees_distribution/<str:id>', edit_fees_distribution.as_view(), name = 'edit_fees_distribution'),
    
]