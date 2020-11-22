from rest_framework import serializers
from patients.serializers import DocDetailSerializer
from .models import DoctorPatientAssociation

class DoctorPatientGetSerializer(serializers.ModelSerializer):
    doctor_id = DocDetailSerializer()
    class Meta:
        model = DoctorPatientAssociation
        fields = ['doctor_id','patient_id','status']

    def to_representation(self, obj):
        represtation = super().to_representation(obj)
        doctor_representation = represtation.pop('doctor_id')
        for key in doctor_representation:
            represtation[key] = doctor_representation[key]
        return represtation

class DoctorPatientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatientAssociation
        fields = ['doctor_id','patient_id','status']