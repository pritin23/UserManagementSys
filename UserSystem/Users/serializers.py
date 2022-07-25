from rest_framework import serializers
from .models import UserDerived
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """
      serializer for user model, by adding password hashing
     """
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = UserDerived
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'date_of_birth', 'email', 'phone_number',
                  'street', 'zip_code', 'city', 'state', 'country']

    # make password in hash format
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = False
        return super(UserSerializer, self).create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer for update the fields
    """

    class Meta:
        model = UserDerived
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'phone_number',
                  'street', 'zip_code', 'city', 'state', 'country']
