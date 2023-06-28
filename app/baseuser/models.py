from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Base(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class User(AbstractUser):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    profile_photo=models.ImageField( default='profile_photos/pp.jpeg' ,upload_to='profile_photos')
    user_type_names=(('s','student'),
                     ('t','teacher'),
                     ('a','admin'),
                     )
    user_type=models.CharField(max_length=500,choices=user_type_names)
