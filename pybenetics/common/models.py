from django.db import models

from pybenetics import settings


class Brand(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()


class Certification(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField(default=0)

    class Meta:
        abstract = True


class EfficiencyCertification(Certification):
    image = models.ImageField(upload_to=settings.MEDIA_URL + "efficiency", blank=True)


class NoiseCertification(Certification):
    image = models.ImageField(upload_to=settings.MEDIA_URL + "noise", blank=True)
