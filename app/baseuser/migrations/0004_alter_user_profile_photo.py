# Generated by Django 4.2.2 on 2023-06-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseuser', '0003_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='images/profile.png', upload_to='profile_photos'),
        ),
    ]
