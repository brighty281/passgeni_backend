from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)


class SavePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model=SavedPasswords
        fields='__all__'