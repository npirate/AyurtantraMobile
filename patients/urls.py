from django.urls import path

from .views import Search_Doctor_API, Doctor_Details_By_Username_API, Add_Bookings_API

urlpatterns = [
    path('search-doctor/',Search_Doctor_API.as_view(),name='search-doctor-url'),
    path('doctor-details-by-username/', Doctor_Details_By_Username_API.as_view(),name='doctor-details-by-username-url'),
    path('add-appt/', Add_Bookings_API.as_view(),name='add-bookings-url')
]