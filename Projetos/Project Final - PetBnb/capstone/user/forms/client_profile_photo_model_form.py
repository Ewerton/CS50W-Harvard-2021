from django import forms
from photo.models.photo import Photo


class ClientProfilePhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            'photo',
        ]

        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
