from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()


class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    create_password_token = serializers.CharField()


class EmailUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    create_username_token = serializers.CharField()
