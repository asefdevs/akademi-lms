# Generated by Django 4.2.2 on 2023-07-15 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_classname_maximum_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classname',
            name='lessons',
        ),
    ]