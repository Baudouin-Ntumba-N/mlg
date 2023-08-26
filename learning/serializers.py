from rest_framework import serializers
from .models import Inscrit
from django.contrib.auth import get_user_model
User = get_user_model()







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrit
        fields = ('id', 'username', 'password')


class InscritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrit
        fields = ('id','username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class EndSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrit
        fields = ('id', 'first_name', 'last_name')