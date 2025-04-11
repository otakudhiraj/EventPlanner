# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from apps.users.forms import UserProfileForm
from apps.venue.models import BookingModel


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile')

class UserBookingView(LoginRequiredMixin, ListView):
    template_name = 'users/user_bookings.html'
    model = BookingModel
    context_object_name = "bookings"

    def get_queryset(self):
        return BookingModel.objects.filter(user=self.request.user)

