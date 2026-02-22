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