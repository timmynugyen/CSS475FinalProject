from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Reservation
from .forms import Frontpage

#Timmy: shows frontpage and gathers form information
def frontpage(request):
    if request.method == 'POST':
        form = Frontpage(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submitted')
    else:
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
