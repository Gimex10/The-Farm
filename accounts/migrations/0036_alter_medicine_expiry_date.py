# Generated by Django 3.2.8 on 2021-11-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20211127_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
