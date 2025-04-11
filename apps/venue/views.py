from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, TemplateView

from apps.venue.forms import BookingForm
from apps.venue.models import City, VenueModel
import json

# Create your views here.
class CityDetail(DetailView):
    model = City
    context_object_name = 'city'
    template_name = 'venue/city_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get('slug')
        city = get_object_or_404(City.objects.prefetch_related("venues"), slug=slug)
        other_cities = City.objects.exclude(slug=slug)
        context.update({
            'city': city,
            'other_cities': other_cities,
        })

        return context

class VenueDetail(DetailView):
    model = VenueModel
    context_object_name = 'venue'
    template_name = 'venue/venue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get('slug')
        venue = get_object_or_404(VenueModel.objects.prefetch_related("images", "prices"), slug=slug)
        related_venues = VenueModel.objects.filter(city=venue.city).exclude(slug=slug)

        context.update({
            'venue': venue,
            'related_venues': related_venues,
        })

        return context

class CityView(TemplateView):
    template_name = 'venue/cities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = City.objects.all()
        context.update({
            'cities': cities,
        })
        return context


class BookingView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body) if request.body else {}
            booking_form = BookingForm(data)

            if booking_form.is_valid():
                booking = booking_form.save()
                return JsonResponse({
                    'success': True,
                    'booking_id': booking.id,
                    'message': 'Booking created successfully'
                }, status=201)

            return JsonResponse({
                'success': False,
                'errors': booking_form.errors.as_json()
            }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

