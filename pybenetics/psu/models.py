from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from common.models import Brand, EfficiencyCertification, NoiseCertification

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Voltage(models.Model):
    value = models.IntegerField(choices=[(115, "115V"), (230, "230V")])

    def __str__(self):
        return f"{self.value}"


class FormFactor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Wattage(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return f"{self.value}"


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PsuEntry(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    voltage = models.ForeignKey(Voltage, on_delete=models.PROTECT)
    form_factor = models.ForeignKey(FormFactor, on_delete=models.PROTECT)
    wattage = models.ForeignKey(Wattage, on_delete=models.PROTECT)
    average_efficiency = models.DecimalField(max_digits=5, decimal_places=3, validators=PERCENTAGE_VALIDATOR)
    average_efficiency_5vsb = models.DecimalField(max_digits=5, decimal_places=3, validators=PERCENTAGE_VALIDATOR)
    vampire_power = models.DecimalField(max_digits=8, decimal_places=7)
    average_power_factor = models.DecimalField(max_digits=4, decimal_places=3)
    average_noise_output = models.DecimalField(max_digits=4, decimal_places=2)
    efficiency_rating = models.ForeignKey(EfficiencyCertification, on_delete=models.PROTECT, null=True, blank=True)
    noise_rating = models.ForeignKey(NoiseCertification, on_delete=models.PROTECT, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField()
    report_short = models.URLField(null=True, blank=True)
    report = models.URLField(null=True, blank=True)
