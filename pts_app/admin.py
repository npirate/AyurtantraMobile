from django.contrib import admin

# Register your models here.

from .models import DoctorPatientAssociation

admin.site.register(DoctorPatientAssociation)
