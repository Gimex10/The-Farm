# Generated by Django 3.2.8 on 2021-11-13 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_vaccination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brooder',
            name='flock',
        ),
        migrations.AddField(
            model_name='flock',
            name='brooder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.brooder'),
        ),
    ]
