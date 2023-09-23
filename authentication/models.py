from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(
        verbose_name="Age", default=15, validators=[MinValueValidator(limit_value=15)]
    )
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    # Make a new member active & staff by default, so it can do CRUD operations
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.username
