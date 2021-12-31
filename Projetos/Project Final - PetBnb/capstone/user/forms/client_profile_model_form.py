from django import forms
from user.models.profile_client import ProfileClient


class ClientProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileClient
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
