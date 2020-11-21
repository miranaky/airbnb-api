from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = "rooms"

router = DefaultRouter()
router.register("", viewset=viewsets.RoomViewset, basename="room")
urlpatterns = router.urls
