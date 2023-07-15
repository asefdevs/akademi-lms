# Generated by Django 4.2.2 on 2023-07-15 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0018_alter_teacher_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_of_lesson', to='staff.teacher'),
        ),
    ]
