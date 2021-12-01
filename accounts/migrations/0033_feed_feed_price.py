# Generated by Django 3.2.8 on 2021-11-25 11:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_remove_sale_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='feed_price',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
    ]
