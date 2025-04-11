from django.contrib import admin

from apps.venue.models import VenueModel, City, VenueImages, Price, BookingModel

# Register your models here.
admin.site.register(VenueModel)
admin.site.register(City)
admin.site.register(VenueImages)
admin.site.register(Price)
admin.site.register(BookingModel)