import io
import tempfile

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import AuditSeriesForm
from .services import audit_series_by_study_df


@require_http_methods(["GET", "POST"])
def audit_series_view(request):
    if request.method == "POST":
        form = AuditSeriesForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["sample"]

            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                for chunk in uploaded.chunks():
                    tmp.write(chunk)
                tmp.flush()
                df = audit_series_by_study_df(tmp.name)

            text_buffer = io.StringIO()
            # You can choose sep="\t" or sep="," depending on your text format
            df.to_csv(text_buffer, sep="\t", index=False)
            text_buffer.seek(0)

            response = HttpResponse(text_buffer.getvalue(), content_type="text/plain; charset=utf-8")
            response["Content-Disposition"] = 'attachment; filename="audit_results.txt"'
            return response

    else:
        form = AuditSeriesForm()

    return render(request, "pacs_toolkit/audit_series.html", {"form": form})


def index(request):
    return HttpResponse("Hello, world. You're at the PACS Toolkit index.")
