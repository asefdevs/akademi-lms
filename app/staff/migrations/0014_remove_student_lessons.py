# Generated by Django 4.2.2 on 2023-07-15 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0013_remove_student_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='lessons',
        ),
    ]