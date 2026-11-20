from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('O cliente deve ter um nome.')
        return value

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError('O cliente deve ter um email.')
        return value