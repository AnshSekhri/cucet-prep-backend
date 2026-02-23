from django.urls import path
from .views import InitiatePaymentView, VerifyPaymentView

urlpatterns = [
    path('initiate/<uuid:course_id>/', InitiatePaymentView.as_view()),
    path('verify/<uuid:payment_id>/', VerifyPaymentView.as_view()),
]