# Generated by Django 3.2.8 on 2021-11-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20211108_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='brooder',
            name='brooder_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
