from django.urls import path
from .views import AvailableSlotsView, BookSlotView , CancelBookingView

urlpatterns = [
    path('slots/', AvailableSlotsView.as_view()),
    path('book/<uuid:slot_id>/', BookSlotView.as_view()),
    path('cancel/<uuid:booking_id>/', CancelBookingView.as_view()),
]