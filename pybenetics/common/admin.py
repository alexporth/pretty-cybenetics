from django.contrib import admin

from .models import Brand, EfficiencyCertification, NoiseCertification


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url"]
    ordering = ["name"]


@admin.register(EfficiencyCertification, NoiseCertification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ["value", "name", "image"]
    ordering = ["value"]
    # def thumbnail(self, obj):
    #     return mark_safe(f'<img src="{obj.image.url}" />')
    #
    # thumbnail.short_description = "Image"
