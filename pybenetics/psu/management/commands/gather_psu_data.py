from django.core.management.base import BaseCommand

from psu.management.commands._brand_page import BrandPage
from psu.management.commands._psu_page import PsuPage


class Command(BaseCommand):
    help = "Displays current time"

    def add_arguments(self, parser):
        parser.add_argument(
            "--brands",
            nargs="+",
            type=str,
            help="List brand names here if you want to only gather PSU data for specific brands",
        )
        parser.add_argument(
            "--start-from",
            type=str,
            help="As brands are analyzed in alphabetical order, "
            "you can write the brand from which you want to start the data gathering",
        )
        parser.add_argument(
            "--end-after",
            type=str,
            help="As brands are analyzed in alphabetical order, "
            "you can write the brand after which you would like to end the data gathering",
        )

    def handle(self, *args, **options):
        psu_efficiency_brands = BrandPage("efficiency")
        psu_efficiency_brands.parse()
        psu_noise_brands = BrandPage("noise")
        psu_noise_brands.parse()
        brands = options["brands"]
        start_from = options["start_from"]
        end_after = options["end_after"]
        start_gathering = False if start_from else True
        stop_gathering = None
        brand_list = brands if not brands else [brand.lower() for brand in brands]
        for brand, url in psu_noise_brands.brand_urls.items():
            if brand_list and brand.lower() not in brand_list:
                continue
            if stop_gathering is False and end_after.lower() != brand.lower():
                stop_gathering = True
            if start_from and start_from.lower() == brand.lower():
                start_gathering = True
            if end_after and end_after.lower() == brand.lower():
                stop_gathering = False
            if not start_gathering or stop_gathering:
                continue
            psu_page = PsuPage(brand=brand, url=url)
            psu_page.parse()
