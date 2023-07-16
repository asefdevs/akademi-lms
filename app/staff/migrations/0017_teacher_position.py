# Generated by Django 4.2.2 on 2023-07-15 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_student_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='position',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_position', to='staff.lesson'),
        ),
    ]