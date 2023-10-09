from django.core.validators import MinValueValidator, MaxValueValidator, StepValueValidator
from django.db import models

from common.models import Brand, EfficiencyCertification, NoiseCertification

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Voltage(models.Model):
    value = models.IntegerField(choices=[(115, "115V"), (230, "230V")])


class FormFactor(models.Model):
    name = models.CharField(max_length=200)


class Wattage(models.Model):
    value = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=200)


class PsuEntry(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    voltage = models.ForeignKey(Voltage, on_delete=models.PROTECT)
    form_factor = models.ForeignKey(FormFactor, on_delete=models.PROTECT)
    wattage = models.ForeignKey(Wattage, on_delete=models.PROTECT, validators=[StepValueValidator(limit_value=50)])
    average_efficiency = models.DecimalField(max_digits=5, decimal_places=3, validators=PERCENTAGE_VALIDATOR)
    average_efficiency_5vsb = models.DecimalField(max_digits=5, decimal_places=3, validators=PERCENTAGE_VALIDATOR)
    vampire_power = models.DecimalField(max_digits=8, decimal_places=7)
    average_power_factor = models.DecimalField(max_digits=4, decimal_places=3)
    average_noise_output = models.DecimalField(max_digits=4, decimal_places=2)
    efficiency_rating = models.ForeignKey(EfficiencyCertification, on_delete=models.PROTECT, blank=True)
    noise_rating = models.ForeignKey(NoiseCertification, on_delete=models.PROTECT, blank=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField()
    report_short = models.URLField()
    report = models.URLField()
