import datetime
from django import forms
from django.contrib.admin.helpers import ActionForm
from django.forms import SelectDateWidget


class SetCertificationDateForm(ActionForm):
    certification_date = forms.DateField(
        widget=SelectDateWidget,
        initial=(datetime.date.today())
    )
