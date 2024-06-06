from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Reservation, TimeSlot,  Customer, Service, ServiceType, PoolOption, RoomOption

#Adonyas: To access the total cost form admin reservations page
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'timeslot', 'total_cost_link')
    filter_horizontal = ('service',)

    def total_cost_link(self, obj):
        url = reverse('cost', args=[obj.id]) 
        return format_html('<a href="{}">Total Cost</a>', url)
    total_cost_link.short_description = 'Total Cost'


# Register your models here.
admin.site.register(Customer)
admin.site.register(TimeSlot)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(PoolOption)
admin.site.register(RoomOption)
