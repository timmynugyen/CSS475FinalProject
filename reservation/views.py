from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Reservation

def index(request):
    return HttpResponse(f"This is the view section <a href='cost'>click to go to cost</a>")

# list all ids
def cost(request):
    return HttpResponse(f"some reservations may not exist...<br>This is the view section <a href='0'>reservation 0</a><br>This is the view section <a href='1'>reservation 1</a><br><br>This is the view section <a href='2'>reservation 2</a><br>")

# specific id
def costid(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    print(reservation)
    total_cost = reservation.cost()
    return HttpResponse(f"The total cost for reservation {reservation_id} is ${total_cost:.2f}")
