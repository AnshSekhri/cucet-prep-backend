from django.shortcuts import render

# Create your views here.
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer
from courses.models import Course, Enrollment
import hmac
import hashlib
from django.conf import settings


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # 🚫 Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {"message": "You have already purchased this course."},
                status=400
            )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            status="PENDING"
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=201)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(pk=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.status == "SUCCESS":
            return Response({"message": "Payment already verified"})

        received_signature = request.data.get("signature")

        # Generate expected signature
        message = f"{payment.id}|{payment.amount}"
        secret = settings.PAYMENT_GATEWAY_SECRET.encode()

        expected_signature = hmac.new(
            secret,
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(received_signature, expected_signature):
            return Response(
                {"error": "Invalid payment signature"},
                status=400
            )

        # If signature valid
        payment.status = "SUCCESS"
        payment.transaction_id = str(uuid.uuid4())
        payment.save()

        Enrollment.objects.get_or_create(
            user=request.user,
            course=payment.course
        )

        return Response({"message": "Payment verified and course unlocked"})    