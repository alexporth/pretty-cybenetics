from django.http import HttpResponse
from django.template import loader

from .models import PsuEntry


def index(request):
    psu_fields = [field.name for field in PsuEntry._meta.get_fields()]
    psu_entries = PsuEntry.objects.order_by("-brand")
    template = loader.get_template("index.html")
    context = {
        "psu_fields": psu_fields,
        "psu_entries": psu_entries,
    }
    return HttpResponse(template.render(context, request))
