# Generated by Django 4.1.7 on 2023-04-04 18:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0013_remove_address_zip_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="name",
        ),
        migrations.RemoveField(
            model_name="address",
            name="phone",
        ),
    ]