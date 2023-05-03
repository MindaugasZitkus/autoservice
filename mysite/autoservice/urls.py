from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vehicles/', views.vehicles, name="vehicles"),
    path('vehicles/<int:vehicle_id>', views.vehicle, name='vehicle'),
    path('orders/', views.OrderListView.as_view(), name = 'orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
]