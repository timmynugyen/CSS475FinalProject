from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Reservation, Customer, TimeSlot, PoolOption, ServiceType, Service, RoomOption
from .forms import Frontpage

#Timmy: shows frontpage and gathers form information
def frontpage(request):
    if request.method == 'POST':
        form = Frontpage(request.POST)
        if form.is_valid():
            
            input_first_name = form.cleaned_data.get('first_name')
            input_last_name = form.cleaned_data.get('last_name')
            input_email = form.cleaned_data.get('email')
            input_phone_number = form.cleaned_data.get('phone_number')
            service_types = form.cleaned_data.get('service_type')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            room_name = form.cleaned_data.get('room_name')
            input_room_attendees = form.cleaned_data.get('room_attendees')
            input_room_special_orders = form.cleaned_data.get('room_special_orders')
            pool_name = form.cleaned_data.get('pool_name')
            input_pool_attendees = form.cleaned_data.get('pool_attendees')
            input_pool_special_orders = form.cleaned_data.get('pool_special_orders')
            input_is_exclusive = form.cleaned_data.get('is_exclusive')

            #Checks if email already associated with existing customer, otherwise creates new customer
            input_customer, created = Customer.objects.get_or_create(
                email=input_email,
                defaults={
                    'first_name': input_first_name,
                    'last_name': input_last_name,
                    'phone_number': input_phone_number
                }
            )

            #Creates timeslot object
            input_timeslot = TimeSlot.objects.create(start_time=start_time, end_time=end_time)
            
            #Creates pool_option object
            pool_option = None
            #sets to none, otherwise sets to selected pool
            if 'pool' in service_types:
                #creates pool_object based on selected pool
                pool_option = PoolOption.objects.create(
                    pool_name = pool_name,
                    attendees = input_pool_attendees or 0,
                    timeslot = input_timeslot,
                    special_orders = input_pool_special_orders
                )
            
            #Creates room_option object
            room_option = None
            #sets to none ,otherwise sets to selected room
            if 'room' in service_types:
                #creates room_option object base on selected room
                room_option = RoomOption.objects.create(
                    room_name = room_name,
                    attendees = input_room_attendees or 0,
                    timeslot = input_timeslot,
                    special_orders = input_room_special_orders
                )
            
            #Adonyas: creates service_type object based on pool/room options
            service_type = ServiceType.objects.create(
                pool_option = pool_option,
                room_option = room_option
            )

             #Adonyas: creates service object
            service = Service.objects.create()
            service.service_type.add(service_type)
            service.save()

            #Adonyas: takes all info and creates reservation
            reservation = Reservation.objects.create(
                customer = input_customer,
                timeslot = input_timeslot,
                is_exclusive = input_is_exclusive
            )
            reservation.service.add(service)
            reservation.save()
            
            return redirect('submitted', reservation_id=reservation.id)
        else:
            #returns error page if any errors thrown
            errors = form.errors.get('__all__', [])
            return render(request, 'error.html', {'errors': errors})
    else:
        form = Frontpage()
        
    return render(request, "frontpage.html", {'form': form})

#Timmy: redirects to submitted page
#Adonyas: modified the code to display relevant information.
def submitted(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_cost = reservation.cost()  # Ensure this method exists and returns the cost

    context = {
        'total_cost': total_cost,
        'reservation': reservation,
        'reservation_id': reservation_id,
        'message': "Bring the total cost amount when you come to your reservation. We accept cash, debit, and credit cards."
    }

    return render(request, "submitted.html", context)

def index(request):
    return render(request, "index.html")


#Adonyas: added cost and cancel reservation feature
def cost(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_cost = reservation.cost()
    reservations_page_url = '/admin/reservation/reservation/'
    return HttpResponse(
        f"The total cost for reservation {reservation_id} is ${total_cost:.2f}<br>"
        f"<a href='{reservations_page_url}'>Go back to reservations</a>")

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        # Delete related objects
        timeslot = reservation.timeslot
        
        for service in reservation.service.all():
            for service_type in service.service_type.all():
                if service_type.pool_option:
                    service_type.pool_option.delete()
                if service_type.room_option:
                    service_type.room_option.delete()
                service_type.delete()
            service.delete()
        reservation.delete()
        timeslot.delete()
    

        return render(request, "cancel_success.html", {'reservation_id': reservation_id})
    
    return render(request, "cancel_confirm.html", {'reservation': reservation})
