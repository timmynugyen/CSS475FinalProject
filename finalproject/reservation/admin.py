from django.contrib import admin

from .models import Reservation
from .models import ReservationStatus
from .models import TimeSlot
from .models import Payment
from .models import PaymentMethod
from .models import Customer
from .models import Service
from .models import ServiceType

# Register your models here.
admin.site.register(Customer)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(TimeSlot)
admin.site.register(ReservationStatus)
admin.site.register(Reservation)
admin.site.register(ServiceType)
admin.site.register(Service)
