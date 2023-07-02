from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=250, choices=gender_choice)
    birthdate = models.DateField()
    profile_photo = models.ImageField(default='profile_photos/default_pp.png', upload_to='profile_photos')
    user_type_names = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=500, choices=user_type_names)
    country = models.CharField(max_length=250)
    number = models.CharField(max_length=50,blank=True ,null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Users'


