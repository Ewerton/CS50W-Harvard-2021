from django import forms
from photo.models.photo import Photo


class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['user', 'photo']

        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

"""
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
"""