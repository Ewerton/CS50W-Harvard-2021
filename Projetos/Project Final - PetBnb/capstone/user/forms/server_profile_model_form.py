from django import forms
from user.models.profile_server import ProfileServer
from pet_type.models.pet_type import PetType


class ServerProfileModelForm(forms.ModelForm):

    pet_type = forms.MultipleChoiceField(
        choices=list((pt.id, str(pt.get_type)) for pt in PetType.objects.all()),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ProfileServer
        fields = [
            'name',
            'description',
            'pet_type',
            'latitude',
            'longitude'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control' }),
            'longitude': forms.NumberInput(attrs={'class': 'form-control' }),
        }
