from rest_framework import serializers


class FacebookSerializer(serializers.Serializer):
    access_token = serializers.CharField()
