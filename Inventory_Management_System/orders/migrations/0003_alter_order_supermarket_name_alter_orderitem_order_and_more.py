# Generated by Django 5.1.7 on 2025-03-20 22:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='supermarket_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order'),
        ),
        migrations.AlterModelTable(
            name='order',
            table='orders',
        ),
    ]
