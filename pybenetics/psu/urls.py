from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/psu", views.PsuEntryList.as_view()),
    path("api/psu/<int:pk>/", views.PsuEntryDetail.as_view()),
]
