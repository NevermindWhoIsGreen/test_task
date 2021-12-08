import json
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Driver, Vehicle
from .serializers import DriverSerializer, VehicleSerializer


class RestFixtures(TestCase):
    fixtures = ['rest_fixtures.json']

    def test_fixtures_exists(self):
        self.assertTrue(Driver.objects.exists())
        self.assertTrue(Vehicle.objects.exists())


class RestDriverTest(RestFixtures):

    def test_driver_list(self):
        """
        + GET /drivers/driver/ - вивід списку водіїв
        """
        response = self.client.get(reverse('driver-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_driver_list_created_at(self):
        """
        + GET /drivers/driver/?created_at__gte=10-11-2021 - вивід списку водіїв, які створені після 10-11-2021
        + GET /drivers/driver/?created_at__lte=16-11-2021 - вивід списку водіїв, котрі створені до 16-11-2021
        """
        response = self.client.get(f"{reverse('driver-list')}?created_at__gte=10-11-2021")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drivers_created_at = Driver.objects.filter(created_at__gte=datetime.strptime('10-11-2021', '%d-%m-%Y'))
        serializer = DriverSerializer(drivers_created_at, many=True)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(f"{reverse('driver-list')}?created_at__lte=16-11-2021")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drivers_created_at = Driver.objects.filter(created_at__lte=datetime.strptime('16-11-2021', '%d-%m-%Y'))
        serializer = DriverSerializer(drivers_created_at, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_driver_data(self):
        """
        + GET /drivers/driver/<driver_id>/ - отримання інформації по певному водію
        """
        driver = Driver.objects.get(id=1)
        response = self.client.get(reverse('driver-detail', kwargs={'pk': driver.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = DriverSerializer(driver)
        self.assertEqual(response.data, serializer.data)
        # 404
        response = self.client.get(reverse('driver-detail', kwargs={'pk': 948473}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_driver(self):
        """
        + POST /drivers/driver/ - створення нового водія
        """
        response = self.client.post(
            reverse('driver-list'),
            data=json.dumps({'first_name': 'created', 'last_name': 'driver'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 400
        response = self.client.post(
            reverse('driver-list'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_driver(self):
        """
        + UPDATE /drivers/driver/<driver_id>/ - редагування водія
        """
        driver = Driver.objects.get(id=2)
        response = self.client.patch(
            reverse('driver-detail', kwargs={'pk': driver.pk}),
            data=json.dumps({'last_name': driver.last_name + '_updated'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('last_name'), Driver.objects.get(id=driver.id).last_name)

    def test_delete_driver(self):
        """
        + DELETE /drivers/driver/<driver_id>/ - видалення водія
        """""
        driver = Driver.objects.get(id=2)
        response = self.client.delete(reverse('driver-detail', kwargs={'pk': driver.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(reverse('driver-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VehicleRestTest(RestFixtures):

    def test_vehicle_list(self):
        """
        + GET /vehicles/vehicle/ - вивід списку машин
        """
        response = self.client.get(reverse('vehicle-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_vehicle_list_with_drivers_and_no_drivers(self):
        """
        + GET /vehicles/vehicle/?with_drivers=yes - вивід списку машин з водіями
        + GET /vehicles/vehicle/?with_drivers=no - вивід списку машин без водіїв
        """
        response = self.client.get(f"{reverse('vehicle-list')}?with_drivers=yes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle_with_drivers = Vehicle.objects.filter(driver__isnull=False)
        serializer = VehicleSerializer(vehicle_with_drivers, many=True)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(f"{reverse('vehicle-list')}?with_drivers=no")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle_with_no_drivers = Vehicle.objects.filter(driver__isnull=True)
        serializer = VehicleSerializer(vehicle_with_no_drivers, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_vehicle_data(self):
        """
        + GET /vehicles/vehicle/<vehicle_id> - отримання інформації по певній машині
        """
        vehicle = Vehicle.objects.get(id=1)
        response = self.client.get(reverse('vehicle-detail', kwargs={'pk': vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = VehicleSerializer(vehicle)
        self.assertEqual(response.data, serializer.data)
        # 404
        response = self.client.get(reverse('driver-detail', kwargs={'pk': 948473}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vehicle(self):
        """
        + POST /vehicles/vehicle/ - створення нової машини
        """
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps({'driver': 1, 'make': 'D1', 'model': 'D1d', 'plate_number': 'DD 3333 RR'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 400
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check plate_number
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps({'driver': 1, 'make': 'D1', 'model': 'D1d', 'plate_number': 'A223DF23'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = response.data.get('plate_number')[0]
        self.assertEqual(error.code, 'invalid')
        self.assertEqual(error, 'This value does not match the required pattern.')

    def test_update_vehicle(self):
        """
        + UPDATE /vehicles/vehicle/<vehicle_id>/ - редагування машини
        """
        vehicle = Vehicle.objects.get(id=2)
        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk': vehicle.pk}),
            data=json.dumps({'plate_number': 'PP 2321 BB'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('plate_number'), Vehicle.objects.get(id=vehicle.id).plate_number)

    def test_delete_vehicle(self):
        """
        + DELETE /vehicles/vehicle/<vehicle_id>/ - видалення машини
        """""
        vehicle = Vehicle.objects.get(id=2)
        response = self.client.delete(reverse('driver-detail', kwargs={'pk': vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(reverse('driver-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_in_the_car(self):
        """
        + POST /vehicles/set_driver/<vehicle_id>/ - садимо водія в машину / висаджуємоводія з машини
        """""
        vehicle = Vehicle.objects.get(id=6)
        self.assertIsNone(vehicle.driver)
        response = self.client.patch(
            reverse('set_driver-detail', kwargs={'pk': vehicle.pk}),
            data=json.dumps({'driver': 2}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Vehicle.objects.get(id=6).driver)
        self.assertTrue(Vehicle.objects.get(id=6).driver.id, 2)

        response = self.client.patch(
            reverse('set_driver-detail', kwargs={'pk': vehicle.pk}),
            data=json.dumps({'driver': None}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(Vehicle.objects.get(id=6).driver)
