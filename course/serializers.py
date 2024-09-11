from user.serializers import TrainerSerializer 
from rest_framework import serializers  
from .models import Course

# Create your views here.
class CourseSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()  

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'trainer', 'course_duration', 'course_fee', 'class_per_week', 'class_days'] 