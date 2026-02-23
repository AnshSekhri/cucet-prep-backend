from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from rest_framework.generics import RetrieveAPIView
from .models import Enrollment
from .models import Course
from .serializers import CourseSerializer
from users.permissions import IsAdminUserCustom
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from courses.models import CourseContent  


class CourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(
            courses,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

class CourseCreateView(APIView):
    permission_classes = [IsAdminUserCustom]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseSerializer(
            course,
            context={"request": request}
        )

        data = serializer.data

        # If not unlocked → hide full content
        if not data.get("is_unlocked"):
            data["full_content"] = "🔒 Purchase this course to unlock full content."

        return Response(data)    
     
    
class ViewCourseContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, content_id):

        try:
            content = CourseContent.objects.get(pk=content_id)
        except CourseContent.DoesNotExist:
            return Response({"error": "Content not found"}, status=404)

        # Admin override
        if not request.user.is_admin_user:
            is_enrolled = Enrollment.objects.filter(
                user=request.user,
                course=content.course
            ).exists()

            if not is_enrolled:
                return Response(
                    {"error": "You must purchase this course to access content."},
                    status=403
                )

        response = FileResponse(content.file.open())

        # Show inline in browser (not forced download)
        response["Content-Disposition"] = f'inline; filename="{content.file.name}"'

        # Prevent caching
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response