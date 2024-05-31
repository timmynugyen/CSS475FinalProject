from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Reservation

def index(request):
    return render(request, "index.html")


def cost(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_cost = reservation.cost()
    reservations_page_url = '/admin/reservation/reservation/'
    return HttpResponse(
        f"The total cost for reservation {reservation_id} is ${total_cost:.2f}<br>"
        f"<a href='{reservations_page_url}'>Go back to reservations</a>")