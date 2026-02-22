from django.urls import path
from .views import RegisterView , ProtectedView , AdminOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('admin-only/', AdminOnlyView.as_view()),
]
