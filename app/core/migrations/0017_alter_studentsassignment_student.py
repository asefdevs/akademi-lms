# Generated by Django 4.2.2 on 2023-08-07 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_alter_lessons_section'),
        ('core', '0016_alter_studentsassignment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsassignment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_assigment', to='staff.students'),
        ),
    ]
