from rest_framework import serializers
from .models import DocDetail, Appointments, PatientDetail

class DocDetailSerializer(serializers.ModelSerializer):
    doc_id = serializers.IntegerField(source='userid')
    class Meta:
        model = DocDetail
        fields = ['doc_id','username','doc_fname','doc_lname','doc_phone','doc_email']
        #fields = '__all__'

class DoctorPatientGetSerializer(serializers.ModelSerializer):
    userid = DocDetailSerializer()
    class Meta:
        model = PatientDetail
        fields = ['userid','status']

    def to_representation(self, obj):
        represtation = super().to_representation(obj)
        doctor_representation = represtation.pop('userid')
        for key in doctor_representation:
            represtation[key] = doctor_representation[key]
        return represtation


class AppointmentsSerializer(serializers.ModelSerializer):
    #userid = DocDetailSerializer(many=False, read_only= True)
    patientuid = DoctorPatientGetSerializer()
    #print (doctor, ' is the serialized doctor details')
    
    class Meta:
        model = Appointments
        fields = ['patientcomplaint','createddate','patientuid']
        #fields = '__all__'

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        #print (representation)
        doctor_representation = representation.pop('patientuid')
        for key in doctor_representation:
            representation[key] = doctor_representation[key]
        return representation