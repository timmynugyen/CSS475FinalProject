from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def getEmail(self):
        return f"{self.email}"
    
    def getPhoneNumber(self):
        return f"{self.phone_number}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Starts: {self.start_time}, Ends: {self.end_time}"

class ServiceType(models.Model):
    name = models.CharField(max_length=40)
    capacity = models.IntegerField()
    hourlyRate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def getHourlyRate():
        return ServiceType.hourlyRate

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    estimated_people = models.IntegerField()
    is_exclusive = models.BooleanField(default=False)
    service_types = models.ManyToManyField(ServiceType)
    

    def cost(self):
        total_cost = 0
        for service_type in self.service_types.all():
            total_cost += service_type.hourlyRate * self.estimated_people
        return total_cost
    
    def __str__(self):
        return f"Reservation for {self.customer} at {self.timeslot}"

    class Meta:
        unique_together = ('customer', 'timeslot')
