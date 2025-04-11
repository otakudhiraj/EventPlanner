from django.urls import path

from apps.users.views import UserProfileView, UserBookingView

app_name = 'users'
urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('bookings/', UserBookingView.as_view(), name='bookings'),

]