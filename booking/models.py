import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.full_name or self.user.username

class TravelOption(models.Model):
    class TravelType(models.TextChoices):
        FLIGHT = "FLIGHT", "Flight"
        TRAIN  = "TRAIN", "Train"
        BUS    = "BUS",   "Bus"

    travel_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=10, choices=TravelType.choices)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    class Meta:
        ordering = ["departure"]

    def __str__(self):
        return f"{self.get_type_display()} {self.source} → {self.destination} @ {self.departure:%Y-%m-%d %H:%M}"

class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.PROTECT)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONFIRMED)

    class Meta:
        ordering = ["-booking_date"]

    @staticmethod
    @transaction.atomic
    def create_booking(user, travel_option_id, seats:int):
        opt = TravelOption.objects.select_for_update().get(id=travel_option_id)
        if seats < 1:
            raise ValueError("Seats must be at least 1.")
        if opt.available_seats < seats:
            raise ValueError("Not enough seats available.")
        opt.available_seats -= seats
        opt.save(update_fields=["available_seats"])
        total = (opt.price * Decimal(seats)).quantize(Decimal("0.01"))
        return Booking.objects.create(
            user=user, travel_option=opt,
            number_of_seats=seats, total_price=total
        )

    @transaction.atomic
    def cancel(self):
        if self.status == Booking.Status.CANCELLED:
            return
        self.status = Booking.Status.CANCELLED
        self.save(update_fields=["status"])
        opt = TravelOption.objects.select_for_update().get(id=self.travel_option_id)
        opt.available_seats += self.number_of_seats
        opt.save(update_fields=["available_seats"])
