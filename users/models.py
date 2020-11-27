from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    #username = None #should have removed this field before doing the first migration.
    user_type = models.IntegerField(blank=False, default=1)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254, unique=True)