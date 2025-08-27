from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, TravelOption

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "phone")

class TravelFilterForm(forms.Form):
    type = forms.ChoiceField(choices=[("", "Any")] + list(TravelOption.TravelType.choices), required=False)
    source = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}))

class BookingForm(forms.Form):
    seats = forms.IntegerField(min_value=1, label="Number of Seats")
