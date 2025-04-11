from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from apps.venue.constants import FoodType


# Create your models here.
User = get_user_model()

class AbstractSlugModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while type(self).objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class City(AbstractSlugModel):
    image = models.ImageField(upload_to="city/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @property
    def get_venue_count(self):
        qs = VenueModel.objects.filter(city=self)
        return qs.count()

    def __str__(self):
        return self.name


class VenueModel(AbstractSlugModel):
    description = models.TextField(null=True, blank=True)
    capacity = models.PositiveIntegerField()
    thumbnail_image = models.ImageField(upload_to="venue/", null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="venues")
    location_text = models.CharField(max_length=300, null=True, blank=True)
    location_embed = models.TextField(null=True, blank=True)

    available_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def get_veg_price(self):
        qs = Price.objects.get(venue=self, type=FoodType.VEG.value)
        if qs:
            return qs.price
        return None

    @property
    def get_non_veg_price(self):
        qs = Price.objects.get(venue=self, type=FoodType.NON_VEG.value)
        if qs:
            return qs.price
        return None


class Price(models.Model):
    venue = models.ForeignKey(VenueModel, on_delete=models.SET_NULL, null=True, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=FoodType.choices, default=FoodType.VEG, max_length=20)

    def __str__(self):
        return f"{self.type} - price - {self.venue.name}"


class VenueImages(models.Model):
    venue = models.ForeignKey(VenueModel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='venue_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.venue.name} - Image"

class BookingModel(models.Model):
    venue = models.ForeignKey(VenueModel, on_delete=models.SET_NULL, null=True, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bookings")
    total_people = models.PositiveIntegerField(default=0)
    meal_type = models.CharField(choices=FoodType.choices, default=FoodType.VEG, max_length=20)
    booked_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    @property
    def get_total_payment_amount(self):
        price = Price.objects.get(venue=self.venue, type=self.meal_type).price
        return self.total_people * price

    @property
    def get_payment_status_display(self):
        if self.is_paid:
            return "Paid"
        else:
            return "Not Paid"

    def __str__(self):
        return f"{self.venue.name} - {self.user.username} - Booking"

