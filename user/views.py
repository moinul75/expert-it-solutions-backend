from django.shortcuts import render 
from rest_framework import generics,status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
  TokenObtainPairSerializer,
  CustomUserSerializer,
  StudentSerializer,
  TrainerSerializer
  )
from .models import CustomUser,Student,Trainer 
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken





# Create your views here. 
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
   # permission_classes = [IsAuthenticated]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
  #  permission_classes = [IsAuthenticated]

# Trainer Views
class TrainerListCreateView(generics.ListCreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
  #  permission_classes = [IsAuthenticated]

class TrainerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
  #  permission_classes = [IsAuthenticated]