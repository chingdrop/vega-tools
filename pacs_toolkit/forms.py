from django import forms


class AuditSeriesForm(forms.Form):
    sample = forms.FileField(label="Sample Spreadsheet")
