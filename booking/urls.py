from django.contrib import admin
from django.urls import path
from booking import views as v
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
def logout_view(request):
    logout(request)
    return redirect('/')  # redirects to homepage after logout

urlpatterns = [

    # Auth
    path("register/", v.register, name="register"),
    path("login/", v.SignInView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", v.profile, name="profile"),

    # Travel + Booking
    path("", v.travel_list, name="travel_list"),
    path("travel/<int:pk>/", v.travel_detail, name="travel_detail"),
    path("travel/<int:pk>/book/", v.book_now, name="book_now"),
    path("bookings/", v.my_bookings, name="my_bookings"),
    path("bookings/<uuid:booking_id>/cancel/", v.cancel_booking, name="cancel_booking"),
]
