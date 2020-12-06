from django.shortcuts import render
from .models import SPList
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

# Create your views here.

class Any_SP_API (APIView):
    permission_classes = [permissions.AllowAny]
    #id = None

    def post (self, request, format=None, **kwargs):

        sp_params = request.data
        #print (self.kwargs['id'], 'is the keyword argument that the view got')

        #validate your incoming parameter values here
        #if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            #sp_params['get_count'] = 1
        return Response (SPList.objects.sp(id=self.kwargs['id'],data=sp_params))
