# Generated by Django 4.1.7 on 2023-04-11 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_order_pincode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Packed", "Packed"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                ],
                default="new",
                max_length=10,
            ),
        ),
    ]