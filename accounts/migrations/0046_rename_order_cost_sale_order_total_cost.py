# Generated by Django 3.2.8 on 2021-12-02 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='order_cost',
            new_name='order_total_cost',
        ),
    ]