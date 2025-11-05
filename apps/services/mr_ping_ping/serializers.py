from rest_framework import serializers


class ResponseDataSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    success = serializers.BooleanField()
    data = serializers.JSONField()  # Unkown responses from endpoints.


class EndpointResSerializer(serializers.Serializer):
    endpoint = serializers.CharField()
    full_url = serializers.URLField()
    res_time = serializers.FloatField()
    response = ResponseDataSerializer()


class AppStatusSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    endpoints_res = EndpointResSerializer(many=True)


class AppRecordedDataSerializer(serializers.Serializer):
    appName = serializers.CharField()
    app_status = AppStatusSerializer(many=True)
