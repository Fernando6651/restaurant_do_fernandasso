# restaurant/admin.py

from django.contrib import admin
from .models import Reservation, TableAvailability, Dish

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'date', 'number_of_people', 'status')
    list_filter = ('date', 'status')
    search_fields = ('customer_name', 'email')
    ordering = ('-date',)

@admin.register(TableAvailability)
class TableAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'available_tables', 'max_tables')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')
