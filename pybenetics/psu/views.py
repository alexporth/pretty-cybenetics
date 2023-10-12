from django.http import HttpResponse
from django.template import loader
from rest_framework import mixins, generics

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


class PsuEntryList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = PsuEntry.objects.all()
    serializer_class = PsuEntrySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PsuEntryDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = PsuEntry.objects.all()
    serializer_class = PsuEntrySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
