from django import forms
from tailwind.validate import ValidationError

from apps.venue.models import BookingModel


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingModel
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        total_people = cleaned_data.get('total_people')
        venue = cleaned_data.get('venue')

        if venue and total_people:
            if total_people > venue.capacity:
                self.add_error('total_people', f"The venue can only accommodate up to {venue.capacity} people.")

        return cleaned_data
