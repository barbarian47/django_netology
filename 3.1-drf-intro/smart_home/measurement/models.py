from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor,
                                  on_delete=models.CASCADE,
                                  related_name='measurements')
    temperature = models.FloatField()
    created_at = models.DateField(auto_now=True)
    photo = models.ImageField(null=True, blank=True)