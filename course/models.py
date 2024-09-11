from django.db import models

# Refactor to use string reference for ForeignKey
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    trainer = models.ForeignKey('user.Trainer', on_delete=models.CASCADE, related_name='courses')
    course_duration = models.TextField()
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    class_per_week = models.PositiveIntegerField()
    class_days = models.TextField()

    def __str__(self):
        return self.course_name
