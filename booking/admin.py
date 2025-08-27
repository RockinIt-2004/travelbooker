from django.contrib import admin
from .models import TravelOption, Booking, Profile

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ("type", "source", "destination", "departure", "price", "available_seats")
    list_filter = ("type", "source", "destination")
    search_fields = ("source", "destination")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "user", "travel_option", "number_of_seats", "total_price", "status", "booking_date")
    list_filter = ("status",)

admin.site.register(Profile)
