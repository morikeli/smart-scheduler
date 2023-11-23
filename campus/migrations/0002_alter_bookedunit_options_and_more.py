# Generated by Django 4.2.6 on 2023-11-23 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookedunit',
            options={'ordering': ['course_name', 'lecturer'], 'verbose_name_plural': 'Booked units'},
        ),
        migrations.AlterModelOptions(
            name='registeredunit',
            options={'ordering': ['unit', 'student'], 'verbose_name_plural': 'Registered units'},
        ),
        migrations.AlterField(
            model_name='lecturehall',
            name='image',
            field=models.ImageField(default='lecture-hall.jpg', upload_to='Lecture-Halls/img/'),
        ),
    ]