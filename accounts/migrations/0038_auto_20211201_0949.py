# Generated by Django 3.2.8 on 2021-12-01 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_alter_vaccination_flock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='expiry_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='mortality',
            name='flock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.flock'),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='flock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.flock'),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.medicine'),
        ),
    ]
