from django.shortcuts import render
from .models import search_shloka_sp
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

# Create your views here.

class Search_Shloka_API (APIView):
    permission_classes = [permissions.AllowAny]

    def get (self, request, format=None):
        sp_params = request.query_params.dict()
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (search_shloka_sp.objects.sql(sp_params))
