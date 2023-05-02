from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vehicles/', views.vehicles, name="vehicles"),
    path('vehicles/<int:vehicle_id>', views.vehicle, name='vehicle'),
]