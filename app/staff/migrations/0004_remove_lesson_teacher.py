# Generated by Django 4.2.2 on 2023-07-01 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_teacher_teacher_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
    ]
