import json
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Driver, Vehicle
from .serializers import VehicleSerializer


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
        self.assertListEqual([x['id'] for x in response.data], list(drivers.values_list('id', flat=True)))

    def test_driver_list_created_at(self):
        """
        + GET /drivers/driver/?created_at__gte=10-11-2021 - вивід списку водіїв, які створені після 10-11-2021
        + GET /drivers/driver/?created_at__lte=16-11-2021 - вивід списку водіїв, котрі створені до 16-11-2021
        """
        response = self.client.get(f"{reverse('driver-list')}?created_at__gte=10-11-2021")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drivers_created_at = Driver.objects.filter(created_at__gte=datetime.strptime('10-11-2021', '%d-%m-%Y'))
        self.assertListEqual([x['id'] for x in response.data], list(drivers_created_at.values_list('id', flat=True)))

        response = self.client.get(f"{reverse('driver-list')}?created_at__lte=16-11-2021")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drivers_created_at = Driver.objects.filter(created_at__lte=datetime.strptime('16-11-2021', '%d-%m-%Y'))
        self.assertListEqual([x['id'] for x in response.data], list(drivers_created_at.values_list('id', flat=True)))

    def test_get_driver_data(self):
        """
        + GET /drivers/driver/<driver_id>/ - отримання інформації по певному водію
        """
        driver = Driver.objects.get(id=1)
        response = self.client.get(reverse('driver-detail', kwargs={'pk': driver.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), driver.pk)
        # 404
        response = self.client.get(reverse('driver-detail', kwargs={'pk': 948473}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_driver(self):
        """
        + POST /drivers/driver/ - створення нового водія
        """
        data = {'first_name': 'created', 'last_name': 'driver'}
        response = self.client.post(
            reverse('driver-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Driver.objects.filter(**data).exists())

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
        self.assertFalse(Driver.objects.filter(id=driver.pk).exists())

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
        self.assertListEqual([x['id'] for x in response.data], list(vehicles.values_list('id', flat=True)))

    def test_vehicle_list_with_drivers_and_no_drivers(self):
        """
        + GET /vehicles/vehicle/?with_drivers=yes - вивід списку машин з водіями
        + GET /vehicles/vehicle/?with_drivers=no - вивід списку машин без водіїв
        """
        response = self.client.get(f"{reverse('vehicle-list')}?with_drivers=yes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle_with_drivers = Vehicle.objects.filter(driver__isnull=False)
        self.assertListEqual([x['id'] for x in response.data], list(vehicle_with_drivers.values_list('id', flat=True)))

        response = self.client.get(f"{reverse('vehicle-list')}?with_drivers=no")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle_with_no_drivers = Vehicle.objects.filter(driver__isnull=True)
        self.assertListEqual([x['id'] for x in response.data], list(vehicle_with_no_drivers.values_list('id', flat=True)))

    def test_get_vehicle_data(self):
        """
        + GET /vehicles/vehicle/<vehicle_id> - отримання інформації по певній машині
        """
        vehicle = Vehicle.objects.get(id=1)
        response = self.client.get(reverse('vehicle-detail', kwargs={'pk': vehicle.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), vehicle.pk)

        # 404
        response = self.client.get(reverse('driver-detail', kwargs={'pk': 948473}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vehicle(self):
        """
        + POST /vehicles/vehicle/ - створення нової машини
        """
        data = {'driver': 1, 'make': 'D1', 'model': 'D1d', 'plate_number': 'DD 3333 RR'}
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vehicle.objects.filter(**data).exists())

        # 400
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check plate_number
        data_with_wrong_plate_number = {'driver': 1, 'make': 'D1', 'model': 'D1d', 'plate_number': 'A223DF23'}
        response = self.client.post(
            reverse('vehicle-list'),
            data=json.dumps(data_with_wrong_plate_number),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Vehicle.objects.filter(**data_with_wrong_plate_number).exists())
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
        self.assertFalse(Vehicle.objects.filter(id=vehicle.pk).exists())

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
