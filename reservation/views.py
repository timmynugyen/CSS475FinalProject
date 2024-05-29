from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Reservation

def index(request):
    return HttpResponse(f"This is the view section")

def cost(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_cost = reservation.cost()
    return HttpResponse(f"The total cost for reservation {reservation_id} is ${total_cost:.2f}")
