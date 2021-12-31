from django import forms
from user.models.user import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = 'photo',

        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False}),
        }

