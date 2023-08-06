# Generated by Django 4.2.2 on 2023-08-05 16:34

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_alter_lessons_section'),
        ('core', '0004_alter_classes_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name_plural': 'Notifications'},
        ),
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('max_try', models.IntegerField(default=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('receiver', models.ManyToManyField(blank=True, related_name='assignment_receivers', to='staff.students')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigment_creator', to='staff.teachers')),
            ],
            options={
                'verbose_name_plural': 'Assigments',
            },
        ),
    ]
