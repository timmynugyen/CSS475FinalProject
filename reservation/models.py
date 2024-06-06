# written and editted by Adonyas Kibru

from django.db import models
from django.core.exceptions import ValidationError

class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def getFirstName(self):
        return self.first_name
    
    def getLastName(self):
        return self.last_name
    
    def getEmail(self):
        return self.email
    
    def getPhoneNumber(self):
        return self.phone_number
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def getStartTime(self):
        return self.start_time.strftime("%Y-%m-%d %H:%M")
    
    def getEndTime(self):
        return self.end_time.strftime("%Y-%m-%d %H:%M") 
    
    def __str__(self):
        return f"Starts: {self.getStartTime()}, Ends: {self.getEndTime()}"

class RoomOption(models.Model):
    class RoomTypes(models.IntegerChoices):
        ROOM_A = 1, 'Room A'
        ROOM_B = 2, 'Room B'
        ROOM_C = 3, 'Room C'
        ROOM_D = 4, 'Room D'
        NONE = 5, 'Do Not Want a Room'

    room_name = models.IntegerField(choices=RoomTypes.choices, default=RoomTypes.NONE)
    attendees = models.IntegerField(default=0)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, default=0)
    special_orders = models.TextField()


    MAX_ATTENDEES = {
        RoomTypes.ROOM_A: 15,
        RoomTypes.ROOM_B: 30,
        RoomTypes.ROOM_C: 50,
        RoomTypes.ROOM_D: 100,
        RoomTypes.NONE: 0
    }

    def clean(self):
        super().clean()
        max_attendance = self.MAX_ATTENDEES.get(self.room_name, 0)
        if self.attendees > max_attendance:
            raise ValidationError(f"Attendees for {self.get_room_name_display()} cannot exceed {max_attendance}.")
        
    def getAttendees():
        return RoomOption.attendees
    
    def getTimeSlot():
        return RoomOption.timeslot
    
    def getSpecialOrder():
        return RoomOption.special_orders
    
    def __str__(self):
        return f"{self.get_room_name_display()}"

class PoolOption(models.Model):
    class PoolTypes(models.IntegerChoices):
        POOL_A = 1, 'Pool A'
        POOL_B = 2, 'Pool B'
        POOL_C = 3, 'Pool C'
        POOL_D = 4, 'Pool D'
        NONE = 5, 'Do Not Want To Swim'

    pool_name = models.IntegerField(choices=PoolTypes.choices, default=PoolTypes.NONE)
    attendees = models.IntegerField(default=0)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,  default=0)
    special_orders = models.TextField()

    
    MAX_ATTENDEES = {
        PoolTypes.POOL_A: 15,
        PoolTypes.POOL_B: 30,
        PoolTypes.POOL_C: 50,
        PoolTypes.POOL_D: 100,
        PoolTypes.NONE: 0
    }

    def clean(self):
        super().clean()
        max_attendance = self.MAX_ATTENDEES.get(self.pool_name, 0)
        if self.attendees > max_attendance:
            raise ValidationError(f"Attendees for {self.get_pool_name_display()} cannot exceed {max_attendance}.")
        
    def getAttendees():
        return PoolOption.attendees
    
    def getTimeSlot():
        return PoolOption.timeslot
    
    def getSpecialOrder():
        return PoolOption.special_orders
    
    def __str__(self):
        return f"{self.get_pool_name_display()}"

class ServiceType(models.Model):
    room_option = models.ForeignKey(RoomOption, on_delete=models.CASCADE, null=True, blank=True)   
    pool_option = models.ForeignKey(PoolOption, on_delete=models.CASCADE, null=True, blank=True)

    def getid():
        return ServiceType.id
    
    def __str__(self):
        return f"Service Type Room: {self.room_option}, Pool: {self.pool_option}"

class Service(models.Model):
    service_type = models.ManyToManyField(ServiceType)

    def __str__(self):
        return f"Service ID: {self.id}"
    

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_exclusive = models.BooleanField(default=False)
    service = models.ManyToManyField(Service)
    

    def cost(self):
        total_cost = 0
        for service in self.service.all():
            for service_type in service.service_type.all():
                if service_type.room_option:
                    total_cost += service_type.room_option.attendees * 20
                if service_type.pool_option:
                    total_cost += service_type.pool_option.attendees * 20
        if self.is_exclusive:
            total_cost *= 1.5  # Apply the 1.5 multiplier for exclusive reservations
        return total_cost
    
    def __str__(self):
        return f"Reservation for {self.customer} at {self.timeslot}"

    class Meta:
        unique_together = ('customer', 'timeslot')
