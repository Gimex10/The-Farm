# Generated by Django 3.2.8 on 2021-11-30 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_alter_medicine_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccination',
            name='flock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.flock'),
        ),
    ]
