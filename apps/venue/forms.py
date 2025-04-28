from django import forms
from apps.venue.constants import BookingStatus
from apps.venue.models import BookingModel


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingModel
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        total_people = cleaned_data.get('total_people')
        venue = cleaned_data.get('venue')
        booked_for = cleaned_data.get('booked_for')

        if venue and total_people:
            if total_people > venue.capacity:
                self.add_error('total_people', f"The venue can only accommodate up to {venue.capacity} people.")

        is_booked = BookingModel.objects.filter(venue=venue, booked_for=booked_for, status=BookingStatus.PENDING).exists()
        if is_booked:
            self.add_error("booked_for", f"The venue is already booked for: {venue}")

        return cleaned_data
