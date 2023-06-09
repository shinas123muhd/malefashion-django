# Generated by Django 4.1.7 on 2023-04-03 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_remove_userprofile_profile_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_1",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_2",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="city",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="state",
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address_line_1", models.CharField(blank=True, max_length=100)),
                ("address_line_2", models.CharField(blank=True, max_length=100)),
                ("name", models.CharField(blank=True, max_length=100)),
                ("city", models.CharField(blank=True, max_length=20)),
                ("state", models.CharField(blank=True, max_length=20)),
                ("country", models.CharField(blank=True, max_length=20)),
                ("zip_code", models.CharField(blank=True, max_length=10)),
                ("phone", models.CharField(max_length=12)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userprofile",
                    ),
                ),
            ],
        ),
    ]
