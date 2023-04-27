from django.shortcuts import render
from .models import Service, Order, Vehicle


# Create your views here.
def index(request):
    context = {
        "service_count": Service.objects.count(),
        "orders_done": Order.objects.filter(status__exact="i").count(),
        "vehicles": Vehicle.objects.count(),

    }
    return render(request, 'index.html', context=context)
