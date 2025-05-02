from rest_framework import serializers


class PostLoginRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()