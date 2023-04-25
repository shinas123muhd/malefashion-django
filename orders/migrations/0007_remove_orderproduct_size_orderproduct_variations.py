# Generated by Django 4.1.7 on 2023-04-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_variation"),
        ("orders", "0006_alter_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="size",
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="variations",
            field=models.ManyToManyField(blank=True, to="store.variation"),
        ),
    ]
