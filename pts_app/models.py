from django.db import models

# Create your models here.

class DoctorPatientAssociation (models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    status = models.IntegerField (default=1)
    objects = models.Manager()