import io
import tempfile

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from common.pandas_tools import read_structured_file
from .forms import AuditSeriesForm
from .services import audit_series_by_study_df


# noinspection PyTypeChecker
@require_http_methods(["GET", "POST"])
def audit_series_view(request):
    form = AuditSeriesForm(request.POST, request.FILES)
    if form.is_valid():
        uploaded = form.cleaned_data["sample"]
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            for chunk in uploaded.chunks():
                tmp.write(chunk)
            tmp.flush()

        input_df = read_structured_file(tmp.name)
        result_df = audit_series_by_study_df(input_df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            result_df.to_excel(writer, index=False, sheet_name="AuditResults")
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = 'attachment; filename="audit_results.xlsx"'
        return response

    return render(request, "pacs_toolkit/audit_series.html", {"form": form})


# ToDo - Create a homepage where you can navigate the different views in the app.
def index(request):
    return HttpResponse("Hello, world. You're at the PACS Toolkit index.")
