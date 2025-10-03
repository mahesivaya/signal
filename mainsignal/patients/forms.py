from django import forms
from .models import PatientImage

class PatientImageForm(forms.ModelForm):
    class Meta:
        model = PatientImage
        fields = ['file']
