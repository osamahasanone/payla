from rest_framework import serializers


class ClientTransactionSerializer(serializers.Serializer):
    confirmation_url = serializers.URLField(max_length=200, allow_blank=False)
    valid_to = serializers.DateTimeField()
