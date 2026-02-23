from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    is_student = models.BooleanField(default=True)
    is_admin_user = models.BooleanField(default=False)

