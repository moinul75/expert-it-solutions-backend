from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date 
from django.utils.timezone import now
import json 
# CustomUser Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('superadmin', 'Superadmin'),
        ('manager', 'Manager'),
        ('student', 'Student'), 
        ('trainer', 'Trainer'), 
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    permissions = models.TextField(blank=True, null=True)
    
    def get_permissions(self):
        if self.permissions:
            try:
                return json.loads(self.permissions)
            except json.JSONDecodeError:
                return []
        return []

    def __str__(self):
        return self.username 
    
# Trainer Model
class Trainer(models.Model):  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='trainer_profile')
    joining_date = models.DateField(default=date.today)
    phone_number = models.CharField(max_length=15)
    expert_in = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        ordering = ['-joining_date']

    def __str__(self):
        return str(self.user.username)

# Student Model
class Student(models.Model): 
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    joining_date = models.DateField(default=now)  
    mothers_name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='students',null=True)
    course_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    due = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    batch_no = models.CharField(max_length=150)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='students_trainer',null=True)
    blood_group = models.CharField(max_length=3)
    address = models.TextField() 
    note = models.TextField(blank=True, null=True)
    documents = models.ManyToManyField('Document', blank=True)   
    
    
    def save(self, *args, **kwargs):
        if self.course:
            discount_rate = self.course_discount
            discounted_fee = self.course.course_fee * (1 - discount_rate / 100)
            self.due = discounted_fee - self.payment
        super(Student, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-joining_date']

    def __str__(self):
        return self.user.username

class Document(models.Model):
    file = models.FileField(upload_to='student_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"


