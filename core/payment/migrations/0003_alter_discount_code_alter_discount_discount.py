# Generated by Django 5.0.2 on 2024-05-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_discount_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.IntegerField(),
        ),
    ]