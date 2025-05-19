from django.urls import path

from . import views

app_name = "pacs_toolkit"

urlpatterns = [
    path("", views.index, name="index"),
]
