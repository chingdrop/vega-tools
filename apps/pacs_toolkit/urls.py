from django.urls import path

from . import views

app_name = "pacs_toolkit"

urlpatterns = [
    path("", views.index, name="index"),
    path("audit/", views.audit_series_view, name="audit_series"),
]
