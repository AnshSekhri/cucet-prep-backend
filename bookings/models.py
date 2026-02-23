from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class AvailableSlot(models.Model):

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | {self.start_time}-{self.end_time}"


class Booking(models.Model):

    slot = models.OneToOneField(
        AvailableSlot,
        on_delete=models.CASCADE,
        related_name="booking"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    topic = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} booked {self.slot}"