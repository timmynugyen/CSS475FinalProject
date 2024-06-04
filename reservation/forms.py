from django import forms
from .models import Customer, TimeSlot, RoomOption, PoolOption, ServiceType

class Frontpage(forms.ModelForm):
    ServiceChoices = [
        ('pool', 'Pool'),
        ('room', 'Room')
    ]

    service_type = forms.MultipleChoiceField(
        required = True,
        widget = forms.CheckboxSelectMultiple,
        choices = ServiceChoices,
        label = "Select Reservation Type"
    )

    start_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start Time"
    )
    
    end_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Time"
    )
    
    room_name = forms.ChoiceField(
        choices=RoomOption.RoomTypes.choices,
        label="Room Option"
    )
    
    room_attendees = forms.IntegerField(
        required=False,
        label="Room Attendees"
    )
    
    room_special_orders = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Room Special Orders"
    )
    
    pool_name = forms.ChoiceField(
        choices=PoolOption.PoolTypes.choices,
        label="Pool Option"
    )
    
    pool_attendees = forms.IntegerField(
        required=False,
        label="Pool Attendees"
    )
    
    pool_special_orders = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Pool Special Orders"
    )

    is_exclusive = forms.BooleanField(
        required=False,
        label="Exclusive Reservation"
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number']
