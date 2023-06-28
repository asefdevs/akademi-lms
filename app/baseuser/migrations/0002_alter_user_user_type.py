# Generated by Django 4.2.2 on 2023-06-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('s', 'student'), ('t', 'teacher'), ('a', 'admin')], max_length=500),
        ),
    ]
