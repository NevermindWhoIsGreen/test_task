from django.db import models


# + id: int
# + first_name: str
# + last_name: str
# + created_at
# + updated_at
class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Vehicle
# + id: int
# + driver_id: FK to Driver
# + make: str
# + model: str
# + plate_number: str - format example "AA 1234 OO"
# + created_at
# + updated_at
class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, blank=True, null=True, related_name='vehicles', on_delete=models.SET_NULL)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
