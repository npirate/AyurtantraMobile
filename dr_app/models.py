from django.db import models
from patients.models import SPManager

# Create your models here.

class search_shloka_sp (models.Model):
    objects = SPManager('SearchShloka')
    class Meta:
        managed = False