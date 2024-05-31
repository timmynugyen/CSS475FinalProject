from django import forms
from .models import Customer

class Frontpage(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number']