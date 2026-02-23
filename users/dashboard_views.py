from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.timezone import now
from datetime import date

from courses.models import Enrollment, Course
from bookings.models import Booking, AvailableSlot
from payments.models import Payment
from users.models import User
from users.permissions import IsAdminUserCustom
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from courses.models import Enrollment
from courses.serializers import CourseSerializer


class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        enrollments = Enrollment.objects.filter(user=request.user)
        courses = [enrollment.course for enrollment in enrollments]

        serializer = CourseSerializer(
            courses,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    
from bookings.models import Booking


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        bookings = Booking.objects.filter(student=request.user)

        data = [
            {
                "booking_id": booking.id,
                "date": booking.slot.date,
                "start_time": booking.slot.start_time,
                "end_time": booking.slot.end_time,
                "topic": booking.topic
            }
            for booking in bookings
        ]

        return Response(data)    



# ------------------------
# STUDENT DASHBOARD
# ------------------------

class StudentDashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_courses = Enrollment.objects.filter(user=request.user).count()

        bookings = Booking.objects.filter(student=request.user)

        total_bookings = bookings.count()

        today = date.today()

        upcoming_booking = bookings.filter(
            slot__date__gte=today
        ).order_by("slot__date").first()

        past_bookings_count = bookings.filter(
            slot__date__lt=today
        ).count()

        upcoming_data = None

        if upcoming_booking:
            upcoming_data = {
                "date": upcoming_booking.slot.date,
                "start_time": upcoming_booking.slot.start_time,
                "end_time": upcoming_booking.slot.end_time,
                "topic": upcoming_booking.topic
            }

        return Response({
            "total_courses": total_courses,
            "total_bookings": total_bookings,
            "upcoming_booking": upcoming_data,
            "past_bookings_count": past_bookings_count
        })


# ------------------------
# ADMIN DASHBOARD
# ------------------------

class AdminDashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):

        total_students = User.objects.filter(is_student=True).count()

        total_courses = Course.objects.count()

        from django.db.models import Sum

        total_revenue = Payment.objects.filter(
            status="SUCCESS"
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        active_bookings = Booking.objects.filter(
            slot__date__gte=date.today()
        ).count()

        available_slots = AvailableSlot.objects.filter(
            is_booked=False
        ).count()

        return Response({
            "total_students": total_students,
            "total_courses": total_courses,
            "total_revenue": total_revenue,
            "active_bookings": active_bookings,
            "available_slots": available_slots
        })        