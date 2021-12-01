from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from datetime import datetime
# from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from .models import Customer, Feed, FeedUsage, Feedback, Flock, Medicine, Mortality, Order, Vaccination


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'is_staff']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class AddFlockForm(ModelForm):
    class Meta:
        model = Flock
        fields = '__all__'
        labels = {
            'flock_breedtype': 'Breedtype',
            'is_closed': 'Closed',
        }


class OrderCustomerForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['note', 'status', 'is_delivered', 'delivery_date']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class GiveFeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'


class AddMedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

# trial date class


# class MyForm(forms.Form):
#     # get current date
#     now = datetime.now()

#     # format 2021-11-30
#     date_time = now.strftime("%Y-%m-%d")
#     date_field = forms.DateField(widget=DatePicker())
#     date_field_required_with_min_max_date = forms.DateField(
#         required=True,
#         widget=DatePicker(
#             options={
#                 'minDate': '2021-12-1',
#                 'maxDate': '2100-12-1',
#             },
#         ),
#         initial=date_time,
#     )
#     time_field = forms.TimeField(
#         widget=TimePicker(
#             options={
#                 'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
#                 'defaultDate': '1970-01-01T14:56:00'
#             },
#             attrs={
#                 'input_toggle': True,
#                 'input_group': False,
#             },
#         ),
#     )
#     datetime_field = forms.DateTimeField(
#         widget=DateTimePicker(
#             options={
#                 'useCurrent': True,
#                 'collapse': True,
#             },
#             attrs={
#                 'append': 'fa fa-calendar',
#                 'icon_toggle': True,
#             }
#         ),
#     )


class NewVaccinationForm(ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'


class NewMortalityForm(ModelForm):
    class Meta:
        model = Mortality
        fields = '__all__'


class AddFeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = '__all__'
        labels = {
            'feed_quantity': 'Feed quantity in kgs:',
        }


class AddFeedUsageForm(ModelForm):
    class Meta:
        model = FeedUsage
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
        #super(AddFeedUsageForm, self).__init__(*args, **kwargs)
        #self.fields['brooder'].empty_label = "Select"
        #self.fields['flock'].empty_label = "Select"
