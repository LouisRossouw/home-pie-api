from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    account = serializers.CharField()
    active = serializers.BooleanField()


class ConfigSerializer(serializers.Serializer):
    track_accounts = AccountSerializer(many=True)
    poll_interval = serializers.IntegerField()
    poll_range = serializers.CharField()
