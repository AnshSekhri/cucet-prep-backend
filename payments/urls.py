from django.urls import path
from .views import InitiatePaymentView, VerifyPaymentView

urlpatterns = [
    path('initiate/<int:course_id>/', InitiatePaymentView.as_view()),
    path('verify/<int:payment_id>/', VerifyPaymentView.as_view()),
]