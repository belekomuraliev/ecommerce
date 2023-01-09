from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    patronymic = models.CharField(max_length=90)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sender = models.BooleanField(default=False)

    def __str__(self):
        return self.user
