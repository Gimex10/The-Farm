# Generated by Django 3.2.8 on 2021-11-13 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_brooder_brooder_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brooder',
            name='brooder_breed',
        ),
    ]
