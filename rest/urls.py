from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'drivers/driver', views.DriverView, basename='driver')
router.register(r'vehicles/vehicle', views.VehicleView, basename='vehicle')
router.register(r'vehicles/set_driver', views.SetDriverView, basename='set_driver')

urlpatterns = router.urls
