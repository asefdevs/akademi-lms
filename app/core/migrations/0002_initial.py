# Generated by Django 4.2.2 on 2023-07-23 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='student',
            field=models.ManyToManyField(related_name='class_of_students', to='staff.students'),
        ),
    ]
