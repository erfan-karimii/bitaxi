# Generated by Django 5.0.2 on 2024-05-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0003_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driveroffers",
            name="destination",
            field=models.CharField(
                choices=[
                    ("AL", "Alborz"),
                    ("AR", "Ardabil"),
                    ("AE", "Azerbaijan East"),
                    ("AW", "Azerbaijan Wast"),
                    ("BU", "Bushehr"),
                    ("CM", "Chahar Mahaal and Bakhtiari"),
                    ("FA", "Fars"),
                    ("GI", "Gilan"),
                    ("GO", "Golestan"),
                    ("HA", "Hamadan"),
                    ("HO", "Hormozgan"),
                    ("IL", "Ilam"),
                    ("IS", "Isfahan"),
                    ("KE", "Kerman"),
                    ("KM", "Kermanshah"),
                    ("KN", "Khorasan North"),
                    ("KR", "Khorasan Razavi"),
                    ("KS", "Khorasan South"),
                    ("KH", "Khuzestan"),
                    ("KB", "Kohgiluyeh and Boyer-Ahmad"),
                    ("KU", "Kurdistan"),
                    ("LO", "Lorestan"),
                    ("MA", "Markazi"),
                    ("MZ", "Mazandaran"),
                    ("QA", "Qazvin"),
                    ("QO", "Qom"),
                    ("SE", "Semnan"),
                    ("SB", "Sistan and Baluchestan"),
                    ("TH", "Tehran"),
                    ("YZ", "Yazd"),
                    ("ZN", "Zanjan"),
                ],
                max_length=254,
            ),
        ),
        migrations.AlterField(
            model_name="driveroffers",
            name="origin",
            field=models.CharField(
                choices=[
                    ("AL", "Alborz"),
                    ("AR", "Ardabil"),
                    ("AE", "Azerbaijan East"),
                    ("AW", "Azerbaijan Wast"),
                    ("BU", "Bushehr"),
                    ("CM", "Chahar Mahaal and Bakhtiari"),
                    ("FA", "Fars"),
                    ("GI", "Gilan"),
                    ("GO", "Golestan"),
                    ("HA", "Hamadan"),
                    ("HO", "Hormozgan"),
                    ("IL", "Ilam"),
                    ("IS", "Isfahan"),
                    ("KE", "Kerman"),
                    ("KM", "Kermanshah"),
                    ("KN", "Khorasan North"),
                    ("KR", "Khorasan Razavi"),
                    ("KS", "Khorasan South"),
                    ("KH", "Khuzestan"),
                    ("KB", "Kohgiluyeh and Boyer-Ahmad"),
                    ("KU", "Kurdistan"),
                    ("LO", "Lorestan"),
                    ("MA", "Markazi"),
                    ("MZ", "Mazandaran"),
                    ("QA", "Qazvin"),
                    ("QO", "Qom"),
                    ("SE", "Semnan"),
                    ("SB", "Sistan and Baluchestan"),
                    ("TH", "Tehran"),
                    ("YZ", "Yazd"),
                    ("ZN", "Zanjan"),
                ],
                max_length=254,
            ),
        ),
    ]
