from django.contrib import admin 
from .models import CustomUser,Student,Trainer,Document
# Register your models here. 
admin.site.register(CustomUser) 
admin.site.register(Student)
admin.site.register(Trainer) 
admin.site.register(Document)

