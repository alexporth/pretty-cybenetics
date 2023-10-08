from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs):
        pass
