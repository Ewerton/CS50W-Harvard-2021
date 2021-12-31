from django import forms
from availability.models.availability import Availability


class ServerProfileAvailabilityModelForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = [
            'date',
        ]

        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
