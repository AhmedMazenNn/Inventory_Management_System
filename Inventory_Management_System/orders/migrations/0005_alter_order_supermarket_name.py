# Generated by Django 5.1.7 on 2025-03-20 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='supermarket_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
