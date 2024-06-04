from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, RoomOption, PoolOption

class Frontpage(forms.ModelForm):
    ServiceChoices = [
        ('pool', 'Pool'),
        ('room', 'Room')
    ]

    service_type = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=ServiceChoices,
        label="Select Reservation Type"
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
        choices=[],  # Choices set in __init__
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
        choices=[],  # Choices set in __init__
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

    def __init__(self, *args, **kwargs):
        super(Frontpage, self).__init__(*args, **kwargs)
        self.fields['room_name'].choices = RoomOption.objects.all().values_list('id', 'name')
        self.fields['pool_name'].choices = PoolOption.objects.all().values_list('id', 'name')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if end_time and start_time and end_time <= start_time:
            raise ValidationError("End time must be after start time.")

        return cleaned_data
