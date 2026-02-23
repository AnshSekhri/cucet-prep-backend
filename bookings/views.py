from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .models import AvailableSlot, Booking


class AvailableSlotsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        slots = AvailableSlot.objects.filter(is_booked=False)
        data = [
            {
                "id": slot.id,
                "date": slot.date,
                "start_time": slot.start_time,
                "end_time": slot.end_time
            }
            for slot in slots
        ]
        return Response(data)
    
from courses.models import Enrollment
from datetime import date


class BookSlotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slot_id):

        topic = request.data.get("topic")

        if not topic:
            return Response({"error": "Topic is required"}, status=400)

        # 🔒 Check if student is enrolled in at least one course
        if not Enrollment.objects.filter(user=request.user).exists():
            return Response(
                {"error": "You must purchase a course to book a session."},
                status=403
            )

        try:
            slot = AvailableSlot.objects.get(pk=slot_id, is_booked=False)
        except AvailableSlot.DoesNotExist:
            return Response({"error": "Slot not available"}, status=400)

        # 🚫 Prevent multiple future bookings
        existing_future_booking = Booking.objects.filter(
            student=request.user,
            slot__date__gte=date.today()
        ).exists()

        if existing_future_booking:
            return Response(
                {"error": "You already have a future booking."},
                status=400
            )

        Booking.objects.create(
            slot=slot,
            student=request.user,
            topic=topic
        )

        slot.is_booked = True
        slot.save()

        return Response({"message": "Slot booked successfully"}) 
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(
                pk=booking_id,
                student=request.user
            )
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        slot = booking.slot

        booking.delete()

        # 🔓 Reopen slot
        slot.is_booked = False
        slot.save()

        return Response({"message": "Booking cancelled successfully"})    