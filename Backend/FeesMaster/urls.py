from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('bulk_upload_fees_distribution', bulk_upload_fees_distribution.as_view(), name = 'bulk_upload_fees_distribution'),
    path('add_fees_distributions', add_fees_distributions.as_view(), name = 'add_fees_distributions'),
    path('update_fees_distributions', update_fees_distributions.as_view(), name = 'update_fees_distributions'),
    path('delete_fees_distributions', delete_fees_distributions.as_view(), name = 'delete_fees_distributions'),
    path('add_fees_distributions_for_multiple_class', add_fees_distributions_for_multiple_class.as_view(), name = 'add_fees_distributions_for_multiple_class'),
    path('fees_destributiom_list', fees_destributiom_list.as_view(), name = 'fees_destributiom_list'),
    path('get_fees_distributions_details', get_fees_distributions_details.as_view(), name = 'get_fees_distributions_details'),
    path('edit_fees_distributions_for_multiple_class', edit_fees_distributions_for_multiple_class.as_view(), name = 'edit_fees_distributions_for_multiple_class'),
    path('get_student_pending_fees_list', get_student_pending_fees_list.as_view(), name = 'get_student_pending_fees_list'),
    path('get_student_pending_fees_list_by_id', get_student_pending_fees_list_by_id.as_view(), name = 'get_student_pending_fees_list_by_id'),
    
    
    path('pay_student_fees', pay_student_fees.as_view(), name = 'pay_student_fees'),

    
]

