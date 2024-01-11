from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.region}, {self.zip_code}"