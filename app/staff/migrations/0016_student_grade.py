# Generated by Django 4.2.2 on 2023-07-15 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_classname_students'),
        ('staff', '0015_remove_teacher_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.classname'),
        ),
    ]