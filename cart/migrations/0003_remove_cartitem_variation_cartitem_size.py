# Generated by Django 4.1.7 on 2023-04-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0002_cartitem_variation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="variation",
        ),
        migrations.AddField(
            model_name="cartitem",
            name="size",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
