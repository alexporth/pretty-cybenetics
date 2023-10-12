from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/psus", views.psu_entry_list),
]
