# Generated by Django 5.0.2 on 2024-05-03 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customerprofile_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverprofile',
            old_name='photo',
            new_name='image',
        ),
    ]
