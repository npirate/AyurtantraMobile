from rest_framework import serializers

from .models import DoctorPatientAssociation

class DoctorPatientAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatientAssociation
        fields = ['doctor_id','patient_id','status']