from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class EfficiencyCertification(Certification):
    image = models.ImageField(upload_to="efficiency", blank=True)


class NoiseCertification(Certification):
    image = models.ImageField(upload_to="noise", blank=True)
