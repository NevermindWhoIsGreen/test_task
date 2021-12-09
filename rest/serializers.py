from rest_framework import serializers

from rest.models import Driver, Vehicle

from django.conf import settings

SERIALIZE_FIELD_DT = serializers.DateTimeField(format=settings.DATETIME_INPUT_FORMATS, required=False)


class DriverSerializer(serializers.ModelSerializer):
    created_at = SERIALIZE_FIELD_DT
    updated_at = SERIALIZE_FIELD_DT

    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    created_at = SERIALIZE_FIELD_DT
    updated_at = SERIALIZE_FIELD_DT
    plate_number = serializers.RegexField(r'^[A-Z]{2} \d{4} [A-Z]{2}$', max_length=10)

    class Meta:
        model = Vehicle
        fields = '__all__'


class SetDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('driver',)
