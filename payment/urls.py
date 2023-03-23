from django.urls import path

from .views import *

urlpatterns = [
    path('payment-success', payment_success, name='ps'),
    path('payment-failed', payment_failed, name='pf'),
    path('checkout', checkout, name='checkout'),
    path('complete-order', complete_order, name='complete_order')
]
