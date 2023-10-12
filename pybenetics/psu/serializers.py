from rest_framework import serializers

from common.models import Brand, EfficiencyCertification, NoiseCertification
from common.serializers import BrandSerializer, NoiseCertificationSerializer, EfficiencyCertificationSerializer
from .models import PsuEntry, Voltage, Wattage, FormFactor, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)

    def to_representation(self, value):
        return str(value)


class BrandField(serializers.RelatedField):
    def to_representation(self, value):
        return BrandSerializer(value, context=self.context).data


class VoltageField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)


class FormFactorField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)


class WattageField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)


class EfficiencyCertificationField(serializers.RelatedField):
    def to_representation(self, value):
        return EfficiencyCertificationSerializer(value, context=self.context).data


class NoiseCertificationField(serializers.RelatedField):
    def to_representation(self, value):
        return NoiseCertificationSerializer(value, context=self.context).data


class PsuEntrySerializer(serializers.ModelSerializer):
    brand = BrandField(queryset=Brand.objects.all())
    voltage = VoltageField(queryset=Voltage.objects.all())
    wattage = WattageField(queryset=Wattage.objects.all())
    form_factor = FormFactorField(queryset=FormFactor.objects.all())
    efficiency_rating = EfficiencyCertificationField(queryset=EfficiencyCertification.objects.all())
    noise_rating = NoiseCertificationField(queryset=NoiseCertification.objects.all())
    tags = TagSerializer(many=True)

    class Meta:
        model = PsuEntry
        fields = "__all__"
