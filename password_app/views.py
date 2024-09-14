from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import*
from .models import SavedPasswords
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

from django.shortcuts import redirect
from django.conf import settings
from .services import get_user_data
import random,string


class GoogleLoginApi(APIView):
     def get(self, request, *args, **kwargs):
        print('here---')
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)
        validated_data = auth_serializer.validated_data
        print(validated_data)
        user_data = get_user_data(validated_data)
        print(user_data)
        print("#########8****************")
        if(user_data['status']==False):
            return redirect(settings.BASE_FRONTEND_URL)
        try:
            user = User.objects.get(email=user_data['email'])
            if(user.is_active == False):
                redirect_url = f"{settings.BASE_FRONTEND_URL}/login?message='This account in no longer accessible'"
                return redirect(redirect_url)
            # UserProfile.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            refresh['username'] = str(user.username)

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            redirect_url = f"{settings.BASE_FRONTEND_URL}/login?access={access_token}&refresh={refresh_token}"
            return redirect(redirect_url)
        except:
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            base_username = f"{first_name}{last_name}".lower()

            # Generate a unique username
            username = base_username
            while User.objects.filter(username=username).exists():
                unique_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                username = f"{base_username}{unique_suffix}"

            user = User.objects.create(
                email=user_data['email'],
                username=username 
            )
            # UserProfile.objects.get_or_create(user=user)

            refresh = RefreshToken.for_user(user)
            refresh['username'] = str(user.username)

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            redirect_url = f"{settings.BASE_FRONTEND_URL}/login?access={access_token}&refresh={refresh_token}"
            return redirect(redirect_url)


class SaveAndGetMessage(APIView):
    def post(self,request,user_id,*args, **kwargs):
        print("post reached here")
        user=User.objects.get(id=user_id)
        print(request.data)
        data=request.data.copy()
        data['user']=user.id
        serializer=SavePasswordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,user_id,*args, **kwargs):
        try:    
            user=User.objects.get(id=user_id)
            print("user is......",user)
            passwords=SavedPasswords.objects.filter(user=user)
            serializer=SavePasswordSerializer(passwords,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error':"user not found"},status=status.HTTP_404_NOT_FOUND)
