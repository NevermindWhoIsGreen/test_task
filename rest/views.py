from datetime import datetime

from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin

from .serializers import DriverSerializer, VehicleSerializer, SetDriverSerializer

from .models import Driver, Vehicle


class DriverView(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        query_set = super().get_queryset()
        for filter_name, value in self.request.GET.items():
            if filter_name in ('created_at__gte', 'created_at__lte'):
                query_set = query_set.filter(**{filter_name: datetime.strptime(value, '%d-%m-%Y')})
        return query_set


class VehicleView(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        req_get = self.request.GET
        with_drivers = req_get.get('with_drivers')
        if with_drivers in ('yes', 'no'):
            return self.queryset.filter(driver__isnull=with_drivers == 'no')
        return super().get_queryset()


class SetDriverView(UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = SetDriverSerializer

