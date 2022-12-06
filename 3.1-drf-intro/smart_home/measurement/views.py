from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer, MeasurementsCreateSerializer


class SensorView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementView(CreateAPIView):
    serializer_class = MeasurementsCreateSerializer


class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer