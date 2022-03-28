from django import forms
from .models import Measurements

class MeasurementsModelForm(forms.ModelForm):
    class Meta:
        model = Measurements
        fields = ('destination', )