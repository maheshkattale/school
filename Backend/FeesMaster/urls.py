from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('bulk_upload_fees_distribution', bulk_upload_fees_distribution.as_view(), name = 'bulk_upload_fees_distribution'),
    path('add_fees_distributions', add_fees_distributions.as_view(), name = 'add_fees_distributions'),
    path('update_fees_distributions', update_fees_distributions.as_view(), name = 'update_fees_distributions'),
    path('delete_fees_distributions', delete_fees_distributions.as_view(), name = 'delete_fees_distributions'),
]

