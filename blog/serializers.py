from django.db.models import fields
from django.http import request
from rest_framework import serializers
from rest_framework.response import Response
from .models import Post
from django.contrib.auth.models import User


class PostSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['date_posted','author']
       

class RegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }      

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            ) 
        password = self.validated_data['password'] 
        password2 = self.validated_data['password2']  

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match.'})
        user.set_password(password)
        user.save()
        return user          
       