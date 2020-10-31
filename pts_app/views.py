from django.shortcuts import render
from .models import DoctorPatientAssociation
from .serializers import DoctorPatientAssociationSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class MyDoctor_API (APIView):
    permission_classes = [permissions.AllowAny]

    def get (self, request, format=None):
        data = request.data
        doctor_qs = DoctorPatientAssociation.objects.filter(patient_id=data.get('patient_id'),status=data.get('status'))
        serializer = DoctorPatientAssociationSerializer(doctor_qs,many=True)
        return Response(serializer.data)

    def post (self, request, format=None):
        serializer = DoctorPatientAssociationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put (self, request, format=None):
        data = request.data
        association_qs = DoctorPatientAssociation.objects.filter(patient_id=data.get('patient_id'),doctor_id=data.get('doctor_id')).first() #.first() here is like select top 1
        serializer = DoctorPatientAssociationSerializer(association_qs,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

