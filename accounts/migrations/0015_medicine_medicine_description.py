# Generated by Django 3.2.8 on 2021-11-08 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20211108_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='medicine_description',
            field=models.TextField(null=True),
        ),
    ]
