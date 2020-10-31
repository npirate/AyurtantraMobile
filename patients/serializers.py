from rest_framework import serializers
from .models import Bookings

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id','userid','book_date','book_timeslot','createddatetime','isactive']