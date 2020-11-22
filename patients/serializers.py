from rest_framework import serializers
from .models import DocDetail, Bookings

class DocDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocDetail
        fields = ['doc_fname','doc_lname','doc_phone']
        #fields = '__all__'


class BookingsSerializer(serializers.ModelSerializer):
    #userid = DocDetailSerializer(many=False, read_only= True)
    userid = DocDetailSerializer()
    #print (doctor, ' is the serialized doctor details')
    
    class Meta:
        model = Bookings
        fields = ['id','userid','book_date','book_timeslot']
        #fields = '__all__'

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        #print (representation)
        doctor_representation = representation.pop('userid')
        for key in doctor_representation:
            representation[key] = doctor_representation[key]
        return representation