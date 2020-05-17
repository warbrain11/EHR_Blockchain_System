from rest_framework import serializers
from blockchain.models import *
from datetime import datetime

class blockchain_serializer(serializers.ModelSerializer):
    class Meta:
        model = blockchain
        fields = ['Hash', 'PreviousHash', 'TimeStamp', 'BlockData']
    
class register_user_serializer(serializers.ModelSerializer):
    #password = serializers.CharField(style = {'input_type': 'password'}, write_only = True)
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            date_of_birth = self.validated_data['date_of_birth'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if(password != password2):
            raise serializears.ValidationError({'password': 'Passwords must match!'})
        
        user.set_password(password)  
        user.save()
        return user
