# Generated by Django 3.2.8 on 2021-11-11 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_remove_brooder_brooder_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.product'),
        ),
    ]