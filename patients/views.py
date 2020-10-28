from django.shortcuts import render
from .models import search_doctor_sp, doctor_details_by_username_sp
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# Create your views here.

class Search_Doctor_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def get (self, request, format=None):
        sp_params = request.data
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (search_doctor_sp.objects.sql(sp_params))

    def post (self, request, format=None):
        return Response( data='POST method is now allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Doctor_Details_By_Username_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def get (self, request, format=None):
        sp_params = request.data
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (doctor_details_by_username_sp.objects.sql(sp_params))

    def post (self, request, format=None):
        return Response( data='POST method is now allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
