from rest_framework import serializers

from .models import Brand, EfficiencyCertification, NoiseCertification


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class EfficiencyCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EfficiencyCertification
        fields = ("name", "image")


class NoiseCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoiseCertification
        fields = ("name", "image")
