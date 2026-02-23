from django.urls import path
from .views import AvailableSlotsView, BookSlotView , CancelBookingView

urlpatterns = [
    path('slots/', AvailableSlotsView.as_view()),
    path('book/<int:slot_id>/', BookSlotView.as_view()),
    path('cancel/<int:booking_id>/', CancelBookingView.as_view()),
]