from django.db import models
from baseuser.models import User
from ckeditor.fields import RichTextField


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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
    grade = models.CharField(max_length=232,choices=GRADE_CHOICES)
    lessons = models.ManyToManyField('Lesson', related_name='students')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Students'    


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField('Student', related_name='students')
    teacher_role=models.ForeignKey('Lesson',on_delete=models.CASCADE ,related_name='teacher_role',null=True)
    about_teacher=RichTextField(null=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Teachers' 

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Lessons' 

