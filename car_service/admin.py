from django.contrib import admin
from .models import Car, CarModel, Service, OrderRow, Order


class CarAdmin(admin.ModelAdmin):
    list_display = ("car_model", "plate_number", "client", "VIN_code")


class OrderRowInline(admin.TabularInline):
    model = OrderRow
    extra = 0  # Turn off placeholders


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_order_row_price", "date", "status", "display_services")
    list_filter = ('status', 'date')
    inlines = [OrderRowInline]
    search_fields = ('id', 'car__client', 'date', 'status')
    list_editable = ('date', 'status')


class OrderRowAdmin(admin.ModelAdmin):
    list_display = ("service", "price", "date", "order")
    search_fields = ('id', 'service__name')

    fieldsets = (
        ('General', {'fields': ('date', 'order')}),
        ('Services', {'fields': ('service', 'price')}),
    )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("make", "model")


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(OrderRow, OrderRowAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
