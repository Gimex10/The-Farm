# Generated by Django 3.2.8 on 2021-11-06 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20211103_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_staff',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
