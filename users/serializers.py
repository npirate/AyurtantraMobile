from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from users.models import CustomUser

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name',''),
            'last_name': self.validated_data.get('last_name','')
        }

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','user_type','first_name','last_name']
        #extra_kwargs = {'first_name':{'required':True,'allow_blank':False},
        #'last_name':{'required':True,'allow_blank':False}}