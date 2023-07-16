# Generated by Django 4.2.2 on 2023-07-16 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0020_alter_student_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ManyToManyField(blank=True, related_name='teacher_of_lesson', to='staff.teacher'),
        ),
    ]