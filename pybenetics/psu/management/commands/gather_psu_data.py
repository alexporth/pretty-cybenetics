from django.core.management.base import BaseCommand

from psu.management.commands._brand_page import BrandPage
from psu.management.commands._psu_page import PsuPage


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs):
        psu_efficiency_brands = BrandPage("efficiency")
        psu_efficiency_brands.parse()
        psu_noise_brands = BrandPage("noise")
        psu_noise_brands.parse()
        start_reading = False
        for brand, url in psu_noise_brands.brand_urls.items():
            if "Micronics" == brand:
                start_reading = True
            if not start_reading:
                continue
            psu_page = PsuPage(brand=brand, url=url)
            psu_page.parse()
