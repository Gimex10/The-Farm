# Generated by Django 3.2.8 on 2021-12-05 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0048_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
    ]