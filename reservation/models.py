from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PaymentMethod(models.Model):
    class PaymentNames(models.IntegerChoices):
        CASH = 1, 'Cash'
        CREDIT_CARD = 2, 'Credit Card'
        DEBIT_CARD = 3, 'Debit Card'

    id = models.AutoField(primary_key=True)
    name = models.IntegerField(choices=PaymentNames.choices, default=PaymentNames.CASH)


class Payment(models.Model):
    is_paid = models.BooleanField(default=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)


class ReservationStatus(models.Model):
    class Status(models.IntegerChoices):
        RESERVED = 1, 'Reserved'
        NOT_RESERVED = 2, 'Not Reserved'

    id = models.AutoField(primary_key=True)
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_RESERVED)

    def __str__(self):
        return f"{self.get_status_display()}"


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Starts: {self.start_time}, Ends: {self.end_time}"


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reservation_status = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    estimated_people = models.IntegerField()
    is_exclusive = models.BooleanField(default=False)
    

    def cost(self):
        services = Service.objects.filter(reservation=self)
        total_cost = 0
        for service in services:
            service_type = service.serviceType
            hourly_rate = service_type.hourlyRate
            total_cost += hourly_rate * self.estimated_people
        return total_cost
    
    def __str__(self):
        return f"Reservation for {self.customer} at {self.timeslot}"

    class Meta:
        unique_together = ('customer', 'timeslot')

class ServiceType(models.Model):
    name = models.CharField(max_length=40)
    capacity = models.IntegerField()
    hourlyRate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def getHourlyRate():
        return ServiceType.hourlyRate

class Service(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    serviceType = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    
     
    def __str__(self):
        return f"{self.id}"
    
    def calculate_cost():
        return ServiceType.getHourlyRate()