from django.forms import ModelForm

from .models import *


class Shippingform(ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['user', ]
