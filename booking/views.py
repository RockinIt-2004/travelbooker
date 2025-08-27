from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware

from .forms import RegisterForm, ProfileForm, TravelFilterForm, BookingForm
from .models import Booking, TravelOption

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("travel_list")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})

class SignInView(LoginView):
    template_name = "auth/login.html"


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/profile.html", {"form": form})

def travel_list(request):
    form = TravelFilterForm(request.GET or None)
    qs = TravelOption.objects.all()
    if form.is_valid():
        t = form.cleaned_data.get("type")
        if t:
            qs = qs.filter(type=t)
        src = form.cleaned_data.get("source")
        if src:
            qs = qs.filter(source__icontains=src)
        dst = form.cleaned_data.get("destination")
        if dst:
            qs = qs.filter(destination__icontains=dst)
        date = form.cleaned_data.get("date")
        if date:
            # match any departure on that calendar date
            start = make_aware(datetime.combine(date, datetime.min.time()))
            end   = make_aware(datetime.combine(date, datetime.max.time()))
            qs = qs.filter(departure__range=(start, end))
    return render(request, "travel/list.html", {"form": form, "travels": qs})

def travel_detail(request, pk:int):
    travel = get_object_or_404(TravelOption, pk=pk)
    form = BookingForm()
    return render(request, "travel/detail.html", {"travel": travel, "form": form})

@login_required
def book_now(request, pk:int):
    travel = get_object_or_404(TravelOption, pk=pk)
    if request.method != "POST":
        return redirect("travel_detail", pk=pk)
    form = BookingForm(request.POST)
    if form.is_valid():
        seats = form.cleaned_data["seats"]
        try:
            booking = Booking.create_booking(request.user, travel.id, seats)
            messages.success(request, f"Booking confirmed. ID: {booking.booking_id}")
            return redirect("my_bookings")
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, "travel/detail.html", {"travel": travel, "form": form})

@login_required
def my_bookings(request):
    current = Booking.objects.filter(user=request.user, status=Booking.Status.CONFIRMED)
    past = Booking.objects.filter(user=request.user, status=Booking.Status.CANCELLED)
    return render(request, "booking/list.html", {"current": current, "past": past})

@login_required
def cancel_booking(request, booking_id:str):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if request.method == "POST":
        booking.cancel()
        messages.info(request, "Booking cancelled and seats returned.")
        return redirect("my_bookings")
    return render(request, "booking/confirm_cancel.html", {"booking": booking})
