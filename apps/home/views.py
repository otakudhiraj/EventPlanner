from django.views.generic import TemplateView
from apps.venue.models import City, VenueModel


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = City.objects.all()
        venues = VenueModel.objects.all()[:8]

        context.update({
            'cities': cities,
            'venues': venues,
        })

        return context
