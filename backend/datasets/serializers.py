from rest_framework import serializers
from .models import Dataset
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class DatasetSerializer(serializers.ModelSerializer):
    # represent uploaded_by as username instead of PK
    uploaded_by = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'uploaded_by', 'csv_file', 'total_rows',
            'avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution', 'cleaned_csv', 'summary_pdf', 'analytics'
        ]
        
        read_only_fields = fields


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
