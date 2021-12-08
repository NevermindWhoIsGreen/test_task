from datetime import datetime

from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin

from .serializers import DriverSerializer, VehicleSerializer, SetDriverSerializer

from .models import Driver, Vehicle


class DriverView(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        # Так как мне нельзя использовать формы "+ Завдання зроблене з допомогою форм не зараховується - вчимося читати ТЗ"
        # использовать django_filters тоже нельзя под капотом будут формы :D
        # с django_filters можно было бы добавить filter_class для вьюшки, немного его подправить, что бы работал с нужными форматами
        # ну или так...
        req_get = self.request.GET
        get_date_gte = req_get.get('created_at__gte')
        get_date_lte = req_get.get('created_at__lte')
        if get_date_gte:
            return self.queryset.filter(created_at__gte=datetime.strptime(get_date_gte, '%d-%m-%Y'))
        elif get_date_lte:
            return self.queryset.filter(created_at__lte=datetime.strptime(get_date_lte, '%d-%m-%Y'))
        return super().get_queryset()


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

