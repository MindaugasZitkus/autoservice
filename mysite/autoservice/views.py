from django.shortcuts import render, get_object_or_404
from .models import Service, Order, Vehicle
from django.views import generic
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    context = {
        "service_count": Service.objects.count(),
        "orders_done": Order.objects.filter(status__exact="i").count(),
        "vehicles": Vehicle.objects.count(),

    }
    return render(request, 'index.html', context=context)


def vehicles(request):
    paginator = Paginator(Vehicle.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_vehicles = paginator.get_page(page_number)
    context = {
        "vehicles": paged_vehicles,
    }
    return render(request, "vehicles.html", context=context)


def vehicle(request, vehicle_id):
    context = {
        "vehicle": get_object_or_404(Vehicle, pk=vehicle_id)
    }
    return render(request, 'vehicle.html', context=context)

class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 2

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'


