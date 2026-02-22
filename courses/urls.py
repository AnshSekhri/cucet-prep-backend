from django.urls import path
from .views import CourseListView, CourseCreateView , CourseDetailView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('create/', CourseCreateView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
]