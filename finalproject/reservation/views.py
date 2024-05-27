from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the reservation")

def cost(request, reservation_id):
    return HttpResponse("Your total cost is: " %reservation_id)
