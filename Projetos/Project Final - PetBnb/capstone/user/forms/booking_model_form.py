from django import forms
from booking.models.booking import Booking


class BookingModelForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = list()
        """
        fields = ['date_of_interest']

        widgets = {
            'date_of_interest': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        """
