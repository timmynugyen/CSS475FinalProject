from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Reservation, ReservationStatus, TimeSlot, Payment, PaymentMethod, Customer, Service, ServiceType

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'timeslot', 'reservation_status', 'total_cost_link')

    def total_cost_link(self, obj):
        url = reverse('cost', args=[obj.id]) 
        return format_html('<a href="{}">Total Cost</a>', url)
    total_cost_link.short_description = 'Total Cost'


# Register your models here.
admin.site.register(Customer)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(TimeSlot)
admin.site.register(ReservationStatus)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)
