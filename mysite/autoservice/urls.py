from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vehicles/', views.vehicles, name="vehicles"),
    path('vehicles/<int:vehicle_id>', views.vehicle, name='vehicle'),
    path('search/', views.search, name='search'),
    path('myorders/', views.MyOrderListView.as_view(), name = 'myorders'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('orders/new', views.OrderCreateView.as_view(), name='order_new'),
]

