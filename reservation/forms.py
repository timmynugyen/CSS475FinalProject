from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, RoomOption, PoolOption, TimeSlot

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

        #checks for invalid start/end times
        if end_time and start_time and end_time <= start_time:
            raise ValidationError("End time must be after start time.")
        
        if start_time.date() != end_time.date():
            raise ValidationError("Reservation time must be on same day.")

        if TimeSlot.objects.filter(start_time__lte= "2020-01-01T00:00", end_time__gte= "2120-01-01T00:00").exists():
            raise ValidationError("Invalid date.")
        
        #checks for existing booking during timeslot
        if TimeSlot.objects.filter(start_time = start_time, end_time = end_time).exists():
            raise ValidationError("The selected time slot is already reserved.")
        
        #check for overlapping timeslot
        if TimeSlot.objects.filter(start_time__gte= start_time, end_time__lte= end_time).exists():
            raise ValidationError("This time slot is overlapping with another.")
        
        


        return cleaned_data
