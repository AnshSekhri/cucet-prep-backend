from django.contrib import admin

# Register your models here.
from .models import AvailableSlot, Booking


@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "start_time", "end_time", "is_booked")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "slot", "created_at")