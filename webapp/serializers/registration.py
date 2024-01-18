from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)


class EmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    verification_code = serializers.CharField()


class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128)
    create_password_token = serializers.CharField()


class EmailUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)
    create_username_token = serializers.CharField()
