# Generated by Django 3.2.8 on 2021-11-18 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20211117_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='is_accepted',
        ),
    ]
