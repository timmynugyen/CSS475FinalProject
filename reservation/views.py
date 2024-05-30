from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Reservation

def index(request):
    return render(request, "index.html")
    return HttpResponse(f"")

# list all ids
def cost(request):
    return render(request, "cost.html")

# specific id
def costid(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    print(reservation)
    total_cost = reservation.cost()
    return HttpResponse(f"The total cost for reservation {reservation_id} is ${total_cost:.2f}")
