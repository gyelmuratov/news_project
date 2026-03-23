from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
# 1
# class User(AbstractUser):
#     photo = models.ImageField()
#     date_of_birth = models.DateTimeField()
#     address = models.TextField(blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

