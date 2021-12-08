from rest_framework import serializers

from rest.models import Driver, Vehicle

from test_task.settings import DATETIME_INPUT_FORMATS

SERIALIZE_FIELD_DT = serializers.DateTimeField(format=DATETIME_INPUT_FORMATS, required=False)


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
