from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import PsuEntry
from .serializers import PsuEntrySerializer


def index(request):
    psu_fields = [field.name for field in PsuEntry._meta.get_fields() if field.name != "id"]
    psu_entries = PsuEntry.objects.order_by("-brand")
    template = loader.get_template("index.html")
    context = {
        "psu_fields": psu_fields,
        "psu_entries": psu_entries,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def psu_entry_list(request):
    """
    List all PSU entries
    """
    if request.method == "GET":
        snippets = PsuEntry.objects.all()
        serializer = PsuEntrySerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
