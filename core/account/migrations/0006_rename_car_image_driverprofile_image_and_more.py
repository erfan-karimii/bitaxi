# Generated by Django 5.0.2 on 2024-05-27 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_driverprofile_image_driverprofile_id_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverprofile',
            old_name='car_image',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='driverprofile',
            name='ID_image',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
