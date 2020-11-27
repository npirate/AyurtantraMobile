from django.urls import path
from .views import Search_Doctor_API, Doctor_Details_By_Username_API, Add_Appt_API, MyDoctor_API, Patient_Appointments_API

urlpatterns = [
    path('search-doctor/',Search_Doctor_API.as_view(),name='search-doctor-url'),
    path('doctor-details-by-username/', Doctor_Details_By_Username_API.as_view(),name='doctor-details-by-username-url'),
    path('my-doctors/',MyDoctor_API.as_view(), name='my-doctors-url'),
    path('add-appt/', Add_Appt_API.as_view(),name='add-bookings-url'),
    path('pt-appt/', Patient_Appointments_API.as_view(),name='pt-aapt-url'),
]