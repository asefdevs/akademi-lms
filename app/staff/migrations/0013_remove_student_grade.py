# Generated by Django 4.2.2 on 2023-07-15 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0012_alter_staff_user_alter_student_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='grade',
        ),
    ]