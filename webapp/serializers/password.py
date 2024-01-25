from rest_framework import serializers


class SetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    password = serializers.CharField(min_length=8, max_length=64)
    create_password_token = serializers.CharField()


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
