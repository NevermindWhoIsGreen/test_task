from rest_framework import serializers

from rest.models import Driver, Vehicle

from django.conf import settings


class DriverSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=settings.DATETIME_INPUT_FORMATS, required=False)
    updated_at = serializers.DateTimeField(format=settings.DATETIME_INPUT_FORMATS, required=False)

    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=settings.DATETIME_INPUT_FORMATS, required=False)
    updated_at = serializers.DateTimeField(format=settings.DATETIME_INPUT_FORMATS, required=False)
    plate_number = serializers.RegexField(r'^[A-Z]{2} \d{4} [A-Z]{2}$', max_length=10)

    class Meta:
        model = Vehicle
        fields = '__all__'


class SetDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('driver',)
