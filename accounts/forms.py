from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import (
    Customer,
    Delivery,
    Feed,
    FeedUsage,
    Feedback,
    Flock,
    Medicine,
    Mortality,
    Order,
    Vaccination,
)


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user", "is_staff"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["delivery_date"]


class AddFlockForm(ModelForm):
    class Meta:
        model = Flock
        fields = "__all__"
        labels = {
            "flock_breedtype": "Breedtype",
            "is_closed": "Closed",
        }


class OrderCustomerForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["note", "status", "is_delivered", "delivery_date"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class GiveFeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"


class AddMedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = "__all__"


class NewVaccinationForm(ModelForm):
    class Meta:
        model = Vaccination
        fields = "__all__"


class NewMortalityForm(ModelForm):
    class Meta:
        model = Mortality
        fields = "__all__"


class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"


class AddFeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = "__all__"
        labels = {
            "feed_quantity": "Feed quantity in kgs:",
        }


class AddFeedUsageForm(ModelForm):
    class Meta:
        model = FeedUsage
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    # super(AddFeedUsageForm, self).__init__(*args, **kwargs)
    # self.fields['brooder'].empty_label = "Select"
    # self.fields['flock'].empty_label = "Select"


class AddressForm(ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"
        labels = {
            "address": "Physical Address (Home Address or Apartment)",
            "street": "Street name (The road connecting to your physical address)",
            "road": "Highway/Major road (Which major road is closest to you)",
        }
