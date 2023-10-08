from django.contrib import admin

from .models import Voltage, FormFactor, Wattage, Tag, PSU


@admin.register(Voltage)
class VoltageAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]


@admin.register(FormFactor)
class FormFactorAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Wattage)
class WattageAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_display = [
        "brand_name",
        "name",
        "voltage",
        "form_factor_name",
        "wattage",
        "average_efficiency",
        "average_efficiency_5vsb",
        "vampire_power",
        "average_power_factor",
        "average_noise_output",
        "efficiency_rating_name",
        "noise_rating_name",
        "get_tags",
        "date",
    ]

    @admin.display(ordering="brand__name")
    def brand_name(self, obj):
        return obj.brand.name

    @admin.display(ordering="form_factor__name")
    def form_factor_name(self, obj):
        return obj.form_factor.name

    @admin.display(ordering="efficiency_rating__name")
    def efficiency_rating_name(self, obj):
        return obj.efficiency_rating.name

    @admin.display(ordering="noise_rating__name")
    def noise_rating_name(self, obj):
        return obj.noise_rating.name

    @admin.display(ordering="tags__name")
    def get_tags(self, obj):
        return "\n".join([tag.name for tag in obj.tags.all()])
