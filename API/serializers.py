
from rest_framework import serializers
from .models import Advisor, NewUser, Booking
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('name', 'photo')

    name = serializers.CharField(max_length=255, required=True, write_only=True)
    photo = serializers.CharField(max_length=1000, required=True, write_only=True)


class AdviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('id', 'name', 'photo')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = NewUser
        fields = ('id', 'email', 'password', 'token')
        read_only_fields = ('id', 'token')

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'id': user.pk,
            'token': user.token
        }


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, write_only=True,
        validators=[UniqueValidator(queryset=NewUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    token = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = NewUser
        fields = ('pk', 'name', 'email', 'password', 'token')
        extra_kwargs = {
            'name': {'required': True},
        }
        read_only_fields = ('pk', 'token')

    def create(self, validated_data):
        user = NewUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('user', 'advisor', 'date')

    user = serializers.PrimaryKeyRelatedField(many=False, queryset=NewUser.objects.all(), write_only=True)
    advisor = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), write_only=True, many=False)

    date = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)


class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'advisor', 'date')
        depth=1
