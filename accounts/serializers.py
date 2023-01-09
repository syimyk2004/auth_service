from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from accounts.send_mail import send_message_to_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=5, write_only=True)
    password2 = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def validate_email(self, data):
        print(data)
        user = User.objects.filter(email=data).exists
        if not user:
            raise serializers.ValidationError(f"Пользователь с почтой {data} уже существует!!!")
        return data

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.pop("password2")
        if password1 != password2:
            raise serializers.ValidationError(f"Пароли не совпадают!!!")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        user = User.objects.create_user(**validated_data, password=password)
        user.is_active = False
        user.save()
        send_message_to_email(user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError({
                "error": "such user doesn't exist!!!"
            })
        if not user.is_active:
            raise serializers.ValidationError("user is not active!!!")
        return {
            "user": user
        }


class LoginTokenSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError({
                "error": "such user doesn't exist!!!"
            })
        if not user.is_active:
            raise serializers.ValidationError("user is not active!!!")
        return {
            "user": user
        }

    def create(self, validated_data):
        user = validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return {
            "token": token
        }

