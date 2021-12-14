from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Flock)
admin.site.register(Brooder)
admin.site.register(Medicine)
admin.site.register(Feed)
admin.site.register(FeedUsage)
admin.site.register(Mortality)
admin.site.register(Sale)
admin.site.register(Feedback)
admin.site.register(Vaccination)
admin.site.register(Delivery)
admin.site.register(Income)
admin.site.register(Expense)
