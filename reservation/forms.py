from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, RoomOption, PoolOption, TimeSlot
from datetime import datetime

#Timmy: frontpage form class
class Frontpage(forms.ModelForm):
    ServiceChoices = [
        ('pool', 'Pool'),
        ('room', 'Room')
    ]

    #creates service_type form
    service_type = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=ServiceChoices,
        label="Select Reservation Type"
    )

    #creates start_time form
    start_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start Time"
    )

    #creates end_time form
    end_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Time"
    )

    #creates room_name form
    room_name = forms.ChoiceField(
        choices=[],
        label="Room Option"
    )

    #creates room_attendees form
    room_attendees = forms.IntegerField(
        required=False,
        label="Room Attendees"
    )

    #creates room_special_order form
    room_special_orders = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Room Special Orders"
    )

    #creates pool_name form
    pool_name = forms.ChoiceField(
        choices=[],
        label="Pool Option"
    )

    #creates pool_attendees form
    pool_attendees = forms.IntegerField(
        required=False,
        label="Pool Attendees"
    )

    #creates pool_special_orders form
    pool_special_orders = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Pool Special Orders"
    )

    #creates is_exclusive form
    is_exclusive = forms.BooleanField(
        required=False,
        label="Exclusive Reservation"
    )

    #creates customer info form
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(Frontpage, self).__init__(*args, **kwargs)
        self.fields['room_name'].choices = RoomOption.RoomTypes.choices
        self.fields['pool_name'].choices = PoolOption.PoolTypes.choices

    def clean(self):
        #cleans data, error checks
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        phone_number = cleaned_data.get('phone_number')

        #Rohan validation checks
        validation_errors = []
        
        if 5 > len(phone_number) or not phone_number.isdigit():
            validation_errors.append(
                ValidationError(
                    ("%(phone)s is not a valid phone number."),
                    params={"phone": phone_number}
                )
            )

        #checks for invalid start/end times
        if end_time and start_time and end_time <= start_time:
            validation_errors.append(
                ValidationError(
                    ("End time must be after start time.")
                )
            )
        
        if start_time.date() != end_time.date():
            validation_errors.append(
                ValidationError(
                    ("Reservation time must be on same day.")
                )
            )

        if start_time.year < 2020:
            validation_errors.append(
                ValidationError(
                    ("%(start)s is not a valid year."),
                    params={"start": start_time.year}
                )
            )
        elif end_time.year > 2120:
            validation_errors.append(
                ValidationError(
                    ("%(end)s is not a valid year."),
                    params={"end":end_time.year}
                )
            )  
        
        #checks for existing booking during timeslot
        if TimeSlot.objects.filter(start_time__gte= start_time, end_time__lte= end_time).exists():
            validation_errors.append(
                ValidationError(
                    ("This time overlaps with a time that has already been reserved.")
                )
            )

        if len(validation_errors) > 0:
            raise ValidationError( validation_errors )
            validation_errors = []

        return cleaned_data
        


