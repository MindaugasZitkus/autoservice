from django.contrib import admin
from .models import (VehicleModel,
                     Service,
                     Vehicle,
                     Order,
                     Order_line)

class OrderLineInLine(admin.TabularInline):
    model = Order_line
    extra = 0

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner_name','vehicle_model','plate','vin']
    list_filter = ['owner_name', 'vehicle_model__make', 'vehicle_model__model']
    search_fields = ['plate', 'vin', 'vehicle_model__make', 'vehicle_model__model']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle','date']
    inlines = [OrderLineInLine]




# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Vehicle,VehicleAdmin )
admin.site.register(Order, OrderAdmin)
admin.site.register(Order_line)
