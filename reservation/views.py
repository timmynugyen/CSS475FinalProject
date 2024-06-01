from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Reservation, Customer, TimeSlot, PoolOption, ServiceType, Service, RoomOption
from .forms import Frontpage

#Timmy: shows frontpage and gathers form information
def frontpage(request):
    if request.method == 'POST':
        form = Frontpage(request.POST)
        if form.is_valid():
            customer = form.save()

            service_types = form.cleaned_data.get('service_type')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            room_name = form.cleaned_data.get('room_name')
            room_attendees = form.cleaned_data.get('room_attendees')
            room_special_orders = form.cleaned_data.get('room_special_orders')
            pool_name = form.cleaned_data.get('pool_name')
            pool_attendees = form.cleaned_data.get('pool_attendees')
            pool_special_orders = form.cleaned_data.get('pool_special_orders')

            #Creates timeslot object
            timeslot = TimeSlot.objects.create(start_time=start_time, end_time=end_time)
            
            #Creates pool_option object
            pool_option = None
            #sets to none, otherwise sets to selected pool
            if 'pool' in service_types:
                #creates pool_object based on selected pool
                pool_option = PoolOption.objects.create(
                    pool_name = pool_name,
                    attendees = pool_attendees or 0,
                    timeslot = timeslot,
                    special_orders = pool_special_orders
                )
            
            #Creates room_option object
            room_option = None
            #sets to none ,otherwise sets to selected room
            if 'room' in service_types:
                #creates room_option object base on selected room
                room_option = RoomOption.objects.create(
                    room_name = room_name,
                    attendees = room_attendees or 0,
                    timeslot = timeslot,
                    special_orders = room_special_orders
                )
            
            #creates service_type object based on pool/room options
            service_type = ServiceType.objects.create(
                pool_option = pool_option,
                room_option = room_option
            )
            
            service = Service.objects.create()
            service.service_type.add(service_type)

            #TODO
            # Create reservation object from gather info above

            return redirect('submitted')
    else:
        #TODO
        #Display error message/error page saying reservation info is incorrect/already exists
        form = Frontpage()
        
    return render(request, "frontpage.html", {'form': form})

#Timmy: redirects to submitted page
def submitted(request):
    return render(request, "submitted.html")

def index(request):
    return render(request, "index.html")

def cost(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_cost = reservation.cost()
    reservations_page_url = '/admin/reservation/reservation/'
    return HttpResponse(
        f"The total cost for reservation {reservation_id} is ${total_cost:.2f}<br>"
        f"<a href='{reservations_page_url}'>Go back to reservations</a>")
