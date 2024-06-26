# Generated by Django 5.0.2 on 2024-04-24 02:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account", "0002_customerprofile_driverprofile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Discount",
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
                ("code", models.CharField(max_length=25)),
                ("discount", models.IntegerField()),
                ("validate_time", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="DiscountUserProfile",
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
                ("is_used", models.BooleanField(default=False)),
                (
                    "customer_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.customerprofile",
                    ),
                ),
                (
                    "discount",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment.discount",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="discount",
            name="customer",
            field=models.ManyToManyField(
                through="payment.DiscountUserProfile", to="account.customerprofile"
            ),
        ),
        migrations.CreateModel(
            name="PayMentLog",
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
                ("cost", models.IntegerField()),
                ("day", models.DateField()),
                ("time", models.TimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[("INCREASE", "INCREASE"), ("DECREASE", "DECREASE")],
                        max_length=25,
                    ),
                ),
                (
                    "message",
                    models.CharField(
                        help_text="شرح حال تراکنش", max_length=360, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
