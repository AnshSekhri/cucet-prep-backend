from django.urls import path
from .dashboard_views import MyCoursesView, MyBookingsView,StudentDashboardSummaryView,AdminDashboardSummaryView

urlpatterns = [
    path('my-courses/', MyCoursesView.as_view()),
    path('my-bookings/', MyBookingsView.as_view()),
    path('student-summary/', StudentDashboardSummaryView.as_view()),
    path('admin-summary/', AdminDashboardSummaryView.as_view()),
]