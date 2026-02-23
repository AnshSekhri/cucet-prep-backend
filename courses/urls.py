from django.urls import path
from .views import CourseListView, CourseCreateView , CourseDetailView ,ViewCourseContentView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('create/', CourseCreateView.as_view()),
    path('<uuid:pk>/', CourseDetailView.as_view()),
    path('content/download/<uuid:content_id>/', ViewCourseContentView.as_view()),
]