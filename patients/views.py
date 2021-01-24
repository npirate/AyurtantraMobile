from django.shortcuts import render
from .models import search_doctor_sp, doctor_details_by_username_sp, add_appt_sp, PatientDetail, Appointments
from users.models import CustomUser
from .serializers import DocDetailSerializer, DoctorPatientGetSerializer, AppointmentsSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
import datetime

# definig a function that can be used in all classes
   
def mob_userid (meta_data):
    in_token = meta_data.get('HTTP_AUTHORIZATION')
    t = Token.objects.get(key=in_token[6:])
    y = t.user_id
    return y    

# Create your views here.

class Search_Doctor_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def post (self, request, format=None):
        sp_params = request.data #if sending parameters in JSON body
        #sp_params = request.query_params.dict() #if sending parameters in url as query string
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (search_doctor_sp.objects.sql(sp_params))

    def get (self, request, format=None):
        #sp_params = request.data #if sending parameters in JSON body
        sp_params = request.query_params.dict() #if sending parameters in url as query string
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (search_doctor_sp.objects.sql(sp_params))

    #def post (self, request, format=None):
        #return Response( data='POST method is now allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Doctor_Details_By_Username_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def post (self, request, format=None):
        sp_params = request.data
        if sp_params.get('get_count') is None or sp_params.get('get_count') == '':
            sp_params['get_count'] = 1
        return Response (doctor_details_by_username_sp.objects.sql(sp_params))

    #def post (self, request, format=None):
        #return Response( data='POST method is now allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

class MyDoctor_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def get (self, request, format=None):
        doctor_qs = PatientDetail.objects.filter(pemail=request.user.email, status=1, userid__isnull=False).select_related('userid')
        serializer = DoctorPatientGetSerializer(doctor_qs,many=True)
        return Response(serializer.data)

    #def post (self, request, format=None):
        #data = request.data
        #data['patient_id'] = mob_userid(request.META)
        #serializer = DoctorPatientAssociationSerializer(data=request.data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #def put (self, request, format=None):
        #data = request.data
        #data['patient_id'] = mob_userid(request.META)
        #association_qs = DoctorPatientAssociation.objects.filter(patient_id=mob_userid(request.META),doctor_id=data.get('doctor_id')).first() #.first() here is like select top 1
        #serializer = DoctorPatientPostSerializer(association_qs,data=data)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data)
        #return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post (self, request, format=None):
        sp_params = request.data
        if sp_params.get('email') is None or sp_params.get('email') == '':
            return Response('email: field is mandatory', status=status.HTTP_428_PRECONDITION_REQUIRED)
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        u = Token.objects.select_related('user').get(key=token)
        #print (u)
        sp_params['Fname'] = u.user.first_name
        sp_params['Lname'] = u.user.last_name
        sp_params['Pemail'] = u.user.email

        try:
            pt = PatientDetail.objects.get(pemail=u.user.email,username_email=sp_params.get('email'))
            pt.modifieddatetime = datetime.datetime.now()
            pt.status = sp_params.get('status')
            pt.save()
            return Response('status: status updated', status=status.HTTP_200_OK)

        except PatientDetail.DoesNotExist:
            sp_params['status'] = 1
            sp_params['modifiedDatetime'] = str(datetime.datetime.now())[:-7] #keys are case sensitive
            sp_params['createdDatetime'] = sp_params.get('modifiedDatetime')
            #print (sp_params['createdDatetime'], sp_params['modifiedDatetime'])
            #print('except section')
            return Response (PatientDetail.add_pt_dr.sql(sp_params))

class Add_Appt_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def post (self, request, format=None):
        sp_params = request.data
        sp_params['PatientUID'] = PatientDetail.objects.values_list('patientuid',flat=True).get(pemail=request.user.email, userid=sp_params.get('dr_id'))
        
        #sp_params['status'] = 'N'
        sp_params['date'], sp_params['time'] = sp_params.get('visitDate').split()
        sp_params['Patcomplaint'] = sp_params['patientcomplaint']

        sp_params.pop('dr_id')
        sp_params.pop('visitDate')
        sp_params.pop('patientcomplaint')
        return Response (add_appt_sp.objects.sql(sp_params))

class Patient_Appointments_API (APIView):
    #permission_classes = [permissions.AllowAny]

    def post (self, request, format=None):
        data = request.data
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

        #bookings_qs = Bookings.objects.select_related('userid').all()

        appts_qs = Appointments.objects.select_related('patientuid__userid').filter(
        patientuid__pemail=request.user.email,
        createddate__gte=start_date, 
        createddate__lte=end_date
        ).order_by('createddate')[:5]

        print (appts_qs.query)

        serializer = AppointmentsSerializer(appts_qs, many = True)

        #print (serializer, 'is the serialized data')
        return Response(serializer.data)

        
        