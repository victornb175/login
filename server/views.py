from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

class PostLoginRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


@extend_schema(
    description="""
    Esta es la ruta del login
    sirve para iniciar session
    """,
    summary="sirve para iniciar session",
    request=PostLoginRequest,
)
@api_view(['POST'])
def login(request):
    serializer = PostLoginRequest(data=request.data)
    serializer.is_valid(raise_exception=True)
    login_raw = serializer.validated_data
    
    user = get_object_or_404(User, username=login_raw.get('username'))
    if not user.check_password(login_raw.get('password')):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
 


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED) 
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    return Response({"message": "esta en el logout!"})


@api_view(['GET'])
def profile(request):
    return Response({"message": "esta en el profile!"})
