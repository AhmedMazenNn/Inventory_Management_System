# Generated by Django 5.1.7 on 2025-03-21 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_product_critical_quantity'),
        ('orders', '0007_alter_orderitem_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
