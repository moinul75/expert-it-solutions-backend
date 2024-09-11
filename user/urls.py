from django.urls import path
from .views import (
    CustomUserCreateView,
    CustomTokenObtainPairView, 
    StudentListCreateView, 
    StudentDetailView, 
    TrainerListCreateView, 
    TrainerDetailView
)

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), 
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('trainers/', TrainerListCreateView.as_view(), name='trainer-list-create'),
    path('trainers/<int:pk>/', TrainerDetailView.as_view(), name='trainer-detail'),
]