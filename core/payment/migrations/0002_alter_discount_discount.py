# Generated by Django 5.0.2 on 2024-05-07 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discount",
            name="discount",
            field=models.IntegerField(unique=True),
        ),
    ]
