from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core import validators
from .models import Profile, Category, Content


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        # Ensure email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=10, required=True, validators=[validators.RegexValidator(r'^\d{10}$', message="Phone number must be exactly 10 digits.")])
    pincode = serializers.CharField(max_length=6, required=True, validators=[validators.RegexValidator(r'^\d{6}$', message="Pincode must be exactly 6 digits.")])
    
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'state', 'country', 'pincode', 'role']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ContentSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'document', 'categories', 'author']
        read_only_fields = ['author']
        
    def validate(self, data):
        required_fields = ['id', 'title', 'body', 'summary', 'document']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: f"Required field."})
        return data

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        content = Content.objects.create(**validated_data)
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            content.categories.add(category)
        return content

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        instance = super().update(instance, validated_data)
        instance.categories.clear()
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)
        return instance

