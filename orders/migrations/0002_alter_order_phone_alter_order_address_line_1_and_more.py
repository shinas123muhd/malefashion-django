# Generated by Django 4.1.7 on 2023-04-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="Phone",
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name="order",
            name="address_line_1",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="order",
            name="address_line_2",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.EmailField(max_length=40),
        ),
    ]