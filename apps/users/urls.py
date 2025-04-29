from django.urls import path

from apps.users.views import UserProfileView, UserBookingView, UserRecentVenuesView

app_name = 'users'
urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('bookings/', UserBookingView.as_view(), name='bookings'),
    path('recent-venues/', UserRecentVenuesView.as_view(), name='recent_venues'),

]