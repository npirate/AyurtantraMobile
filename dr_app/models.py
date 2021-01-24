from django.db import models
from patients.models import SPManager

# Create your models here.

class SPList (models.Model):
    spid = models.PositiveIntegerField(unique=True, db_column='spid')
    spname = models.CharField(unique=True, max_length=500)
    objects = SPManager(SPName='')

class ParameterList (models.Model):
    spid = models.ForeignKey('SPList', to_field='spid', on_delete=models.CASCADE, db_column='spid')
    parameter = models.CharField(max_length=1000, null=False, blank=False)
    ptype = models.IntegerField()






