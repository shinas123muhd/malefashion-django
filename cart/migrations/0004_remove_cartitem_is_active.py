# Generated by Django 4.1.7 on 2023-04-03 03:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0003_remove_cartitem_variation_cartitem_size"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="is_active",
        ),
    ]
