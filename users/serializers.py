from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Automatically make them student
        user.is_student = True
        user.is_admin_user = False
        user.save()
        return user