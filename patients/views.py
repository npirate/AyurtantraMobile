from django.shortcuts import render
from .models import search_doctor_sp, doctor_details_by_username_sp, add_bookings_sp, Bookings
from .serializers import BookingsSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token

# definig a function that can be used in all classes
   
def mob_userid (in_token):
    t = Token.objects.get(key=in_token[6:])
    x = t.user_id
    return x

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

    #def post (self, request, format=None):
        #return Response( data='POST method is now allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Add_Bookings_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def post (self, request, format=None):
        sp_params = request.data
        return Response (add_bookings_sp.objects.sql(sp_params))

class Patient_Bookings_API (APIView):

    def get (self, request, format=None):
        in_token = request.META.get('HTTP_AUTHORIZATION')
        #print (in_token[6:])
        
        data = request.data
        #print (data)
        start_date, end_date = '',''
        if data.get('start_date') is None or data.get('start_date') == '':
            start_date = '1900-01-01'
        else:
            start_date = data.get('start_date')

        #print (start_date)
        
        if data.get('end_date') is None or data.get('end_date') == '':
            end_date = '9999-12-31'
        else:
            end_date = data.get('end_date')       
        #print (end_date)

        bookings_qs = Bookings.objects.filter(patientid=mob_userid(in_token),isactive=1,book_date__gte=start_date, book_date__lte=end_date).order_by('-book_date')

        serializer = BookingsSerializer(bookings_qs, many = True)
        return Response(serializer.data)

        
        