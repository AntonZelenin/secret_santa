from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)


class ResendEmailVerificationCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class EmailVerificationCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    verification_code = serializers.CharField()


class CreateUsernameSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    create_username_token = serializers.CharField()
