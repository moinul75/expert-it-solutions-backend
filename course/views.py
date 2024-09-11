from django.shortcuts import render  
from rest_framework import viewsets
from .models import Course 
from user.models import Trainer 
from .serializers import CourseSerializer

        
        
        
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer