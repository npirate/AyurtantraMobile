from django.db import models
from patients.models import DocDetail

# Create your models here.

class DoctorPatientAssociation (models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.ForeignKey(DocDetail, null= True, on_delete=models.SET_NULL, db_constraint=False, db_column='doctor_id')
    status = models.IntegerField (default=1)
    objects = models.Manager()