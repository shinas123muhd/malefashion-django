# Generated by Django 4.1.7 on 2023-04-12 05:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0020_rename_zip_code_address_pincode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="phone",
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
