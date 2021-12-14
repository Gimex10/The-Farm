from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.db.models.fields import CharField, DateField, TextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.core.exceptions import ValidationError
from annoying.fields import AutoOneToOneField

# Create your models here.

# Creates the Customer class and defines its attributes


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    profile_pic = models.ImageField(
        default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name


# Creates the class Tag used to denote type


class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


# Creates the Products class


class Product(models.Model):
    CATEGORY = (
        ("Broiler", "Broiler"),
        ("Layers", "Layers"),
        ("Feeds", "Feeds"),
        ("Other", "Other"),
    )

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True, validators=[MinValueValidator(1.0)])
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


# Creates the Order class


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=100, null=True, choices=STATUS, default="Pending")
    note = models.CharField(max_length=200, null=True, blank=True)
    order_quantity = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    is_paid = models.BooleanField(default=False, null=True)
    is_accepted = models.BooleanField(default=False, null=True)
    is_delivered = models.BooleanField(default=False, null=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_delivered == True:
            self.delivery_date = datetime.datetime.now()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

# Creates the Brooder class


class Brooder(models.Model):

    brooder_name = models.CharField(max_length=50, null=True)
    is_occupied = models.BooleanField(default=False, null=True)
    last_cleaning_date = models.DateField(null=True)
    capacity = 100

    def __str__(self):
        return self.brooder_name

# Creates the Flock class


class Flock(models.Model):
    BREED_TYPE = (
        ("Broiler", "Broiler"),
        ("Layers", "Layers"),
    )
    flock_breedtype = models.CharField(
        max_length=100, null=True, choices=BREED_TYPE)
    batch_no = models.FloatField(null=True, validators=[
                                 MinValueValidator(1.0)])
    flock_quantity = models.FloatField(
        null=True, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)]
    )
    date_flock_bought = models.DateTimeField(auto_now_add=True, null=True)
    flock_price = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    is_closed = models.BooleanField(default=False, null=True)
    brooder = models.ForeignKey(Brooder, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.flock_breedtype

# Creates the Feedback class


class Feedback(models.Model):

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    feedback_info = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.customer.name

# Creates the Medicine class


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100, null=True)
    medicine_description = models.TextField(null=True)
    medicine_price = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    date_med_bought = models.DateField(auto_now_add=True, null=True)
    expiry_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if self.expiry_date < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
        super(Medicine, self).save(*args, **kwargs)

    def __str__(self):
        return self.medicine_name

# Creates the Feed class


class Feed(models.Model):
    FEED_TYPE = (
        ("Layers Mash", "Layers Mash"),
        ("Broilers Mash", "Broilers Mash"),
        ("Starter", "Starter"),
        ("Finisher", "Finisher"),
    )
    feeds_type = models.CharField(max_length=200, null=True, choices=FEED_TYPE)
    feed_name = models.CharField(max_length=100, null=True)
    date_feed_bought = models.DateField(auto_now_add=True, null=True)
    feed_quantity = models.IntegerField(null=True)
    feed_price = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])

    def __str__(self):
        return self.feed_name

# Creates the Mortality class


class Mortality(models.Model):
    flock = models.ForeignKey(Flock, null=True, on_delete=models.CASCADE)
    mortality_count = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    mortality_date = models.DateField(auto_now_add=True, null=True)

# Creates the Feedusage class


class FeedUsage(models.Model):

    FEED_TYPE = (
        ("Layers Mash", "Layers Mash"),
        ("Broilers Mash", "Broilers Mash"),
        ("Starter", "Starter"),
        ("Finisher", "Finisher"),
    )

    brooder = models.ForeignKey(Brooder, null=True, on_delete=models.SET_NULL)
    flock = models.ForeignKey(Flock, null=True, on_delete=models.SET_NULL)
    feed = models.ForeignKey(Feed, null=True, on_delete=models.SET_NULL)
    feed_quantity_used = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)]
    )
    feed_usage_date = models.DateField(auto_now_add=True, null=True)

# Creates the Sale class


class Sale(models.Model):
    BILLING_STATUS = (
        ("Not Billed", "Not Billed"),
        ("Billed", "Billed"),
    )
    order = AutoOneToOneField(Order, primary_key=True,
                              on_delete=models.CASCADE)
    order_total_cost = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    sale_date = models.DateField(auto_now_add=True, null=True)
    billing_status = models.CharField(
        max_length=100, null=True, choices=BILLING_STATUS)

    def save(self, *args, **kwargs):
        self.order_total_cost = self.order.order_quantity * self.order.product.price
        self.billing_status = "Billed"

        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return self.order.product.name

# Creates the Vaccination class


class Vaccination(models.Model):
    flock = models.ForeignKey(Flock, null=True, on_delete=models.SET_NULL)
    medicine = models.ForeignKey(Medicine, null=True, on_delete=models.CASCADE)
    vaccination_date = DateField(auto_now_add=True, null=True)
    vaccination_description = TextField(null=True)

    def __str__(self):
        return self.flock.flock_breedtype

# Creates the Delivery class


class Delivery(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=75, null=True)
    street = models.CharField(max_length=75, null=True)
    road = models.CharField(max_length=75, null=True)

    def __str__(self):
        return self.customer.name

# Creates the Income class


class Income(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    order_income = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    income_date = models.DateTimeField(auto_now_add=True, null=True)

# Creates the Expense class


class Expense(models.Model):
    expense_desc = models.CharField(max_length=100, null=True)
    expense_amount = models.FloatField(
        null=True, validators=[MinValueValidator(1.0)])
    expense_date = models.DateTimeField(auto_now_add=True, null=True)
