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
    about=models.TextField(max_length=2000,blank=True,null=True)
    gender_choice=(
        ('male','male'),
        ('female','female'),

    )
    gender=models.CharField(max_length=250 ,choices=gender_choice,null=True)
    birthday = models.DateField(null=True)
    profile_photo=models.ImageField( default='profile_photos/default_pp.png' ,upload_to='profile_photos')
    user_type_names=(('student','student'),
                     ('teacher','teacher'),
                     ('admin','admin'),
                     )
    user_type=models.CharField(max_length=500,choices=user_type_names)
    country=models.CharField(max_length=250,null=True)
    number=models.CharField(max_length=50,null=True)  
    GRADE_CHOICES = [
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        ('3', '3rd Grade'),
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
        ('8', '8th Grade'),
        ('9', '9th Grade'),
        ('10', '10th Grade'),
        ('11', '11th Grade'),
    ]
    grade=models.CharField(max_length=2,choices=GRADE_CHOICES)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural=('Users')   

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_detail=models.CharField(max_length=400)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher_details=models.CharField(max_length=300)


