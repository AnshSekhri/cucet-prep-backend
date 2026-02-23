from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def get_is_unlocked(self, obj):
        user = self.context.get("request").user

        if not user.is_authenticated:
            return False

        if user.is_admin_user:
            return True

        return Enrollment.objects.filter(user=user, course=obj).exists()