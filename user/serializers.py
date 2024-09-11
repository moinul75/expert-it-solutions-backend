from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Student,Trainer,Document 
from django.contrib.auth.hashers import make_password 
from django.db import IntegrityError 



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type','picture', 'first_name', 'last_name')

class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data,
        }


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file', 'uploaded_at')

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',allow_null=True, required=False)
    email = serializers.EmailField(source='user.email', read_only=False)
    first_name = serializers.CharField(source='user.first_name', read_only=False)
    last_name = serializers.CharField(source='user.last_name', read_only=False)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    picture = serializers.ImageField(source='user.picture',allow_null=True, required=False)
    documents = DocumentSerializer(many=True, required=False)  
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    course_duration = serializers.CharField(source='course.course_duration', read_only=True)
    course_fee = serializers.CharField(source='course.course_fee', read_only=True) 
    trainer = serializers.PrimaryKeyRelatedField(queryset=Trainer.objects.all())
    trainer_name = serializers.SerializerMethodField() 
    student_name = serializers.SerializerMethodField()

    def get_trainer_name(self, obj):
        if obj.course and obj.course.trainer and obj.course.trainer.user:
            return f"{obj.course.trainer.user.first_name} {obj.course.trainer.user.last_name}"
        return None 
    def get_student_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return None

    class Meta:
        model = Student
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name', 
            'student_name',
            'password',
            'picture',
            'mothers_name',
            'fathers_name',
            'course_name',
            'course_duration',
            'course_fee',
            'phone_number',
            'course_discount',
            'payment',
            'due',
            'batch_no',
            'joining_date', 
            'trainer',
            'trainer_name',
            'documents',  
        ] 
        
        read_only_fields = ['due']

    def create(self, validated_data): 
        print("Validated Data:", validated_data)
        user_data = validated_data.pop('user', {})
        user_data = {
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'picture': user_data.get('picture')
        }

        print("User Data: ",user_data)
        user_password = validated_data.get('password')

        try:
            user = CustomUser.objects.create(**user_data, user_type='student') 
            
            if user_password:
                user.set_password(user_password)
                user.save()
            print("The User : ",user)
            student_data = {
                'mothers_name': validated_data.get('mothers_name'),
                'fathers_name': validated_data.get('fathers_name'),
                'phone_number': validated_data.get('phone_number'),
                'course_discount': validated_data.get('course_discount'),
                'payment': validated_data.get('payment'),
                'batch_no': validated_data.get('batch_no'),
                'joining_date': validated_data.get('joining_date'),
                'trainer': validated_data.get('trainer')
            }

            student = Student.objects.create(user=user, **student_data) 
            print("The Student: ",student)

            documents = validated_data.get('documents', [])
            for document_data in documents:
                Document.objects.create(student=student, **document_data)
            
            return student

        except IntegrityError as e:
            if 'UNIQUE constraint failed: user_customuser.username' in str(e):
                raise serializers.ValidationError({'user_username': ['This username is already taken.']})
            else:
                raise serializers.ValidationError({'non_field_errors': ['Database integrity error: {}'.format(str(e))]})
        except Exception as e:
            raise serializers.ValidationError({'non_field_errors': ['An unexpected error occurred: {}'.format(str(e))]})

    def update(self, instance, validated_data):
        # Handle user updates
        documents_data = validated_data.pop('documents', [])
        user_data = {
            'username': validated_data.pop('user_username', None),
            'email': validated_data.pop('user_email', None),
            'first_name': validated_data.pop('user_first_name', None),
            'last_name': validated_data.pop('user_last_name', None),
            'picture': validated_data.pop('picture', None)
        }
        user_password = validated_data.pop('password', None)

        # Update user fields
        if user_data:
            user = instance.user
            for key, value in user_data.items():
                if value is not None:  # Update only non-null values
                    setattr(user, key, value)
            user.save()

        # Update the password if provided
        if user_password is not None:
            if user_password == '':  # Skip if the password field is left empty
                user_password = instance.user.password
            else:
                instance.user.set_password(user_password)
            instance.user.save()

        instance = super().update(instance, validated_data)

        if documents_data:
            instance.documents.clear()  
            for document_data in documents_data:
                Document.objects.create(**document_data)

        return instance

    
class TrainerSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=False)
    user_email = serializers.EmailField(source='user.email', read_only=False)
    user_first_name = serializers.CharField(source='user.first_name', read_only=False)
    user_last_name = serializers.CharField(source='user.last_name', read_only=False)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    picture = serializers.ImageField(source='user.picture', required=False, allow_null=True)  

    class Meta:
        model = Trainer
        fields = [
            'id',
            'user_username',
            'user_email',
            'user_first_name',
            'user_last_name',
            'password',
            'picture',
            'address',
            'phone_number',
            'expert_in',
            'joining_date',
        ]
        
    def create(self, validated_data):
        user_password = validated_data.pop('password', None)

        try:
            user = CustomUser.objects.create(
                **validated_data,
                user_type='trainer'
            )

            if user_password:
                user.password = make_password(user_password)
                user.save()
            
            trainer = Trainer.objects.create(user=user, **validated_data)
            return trainer
        
        except IntegrityError as e:
            if 'UNIQUE constraint failed: user_customuser.username' in str(e):
                raise serializers.ValidationError({'user_username': ['This username is already taken.']})
            else:
                raise serializers.ValidationError({'non_field_errors': ['Error occurred while creating the user.']}) 
            
            
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        user_password = validated_data.pop('password', None)

        if user_data:
            user = instance.user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

        if user_password is not None:  
            if user_password == '': 
                user_password = instance.user.password
                print("USER PASSWORD: ",user_password)
            instance.user.set_password(user_password)
            instance.user.save()

        instance = super().update(instance, validated_data)

        return instance