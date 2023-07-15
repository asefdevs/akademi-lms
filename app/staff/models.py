from django.db import models
from baseuser.models import User
from ckeditor.fields import RichTextField


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    grade = models.ForeignKey('core.ClassName', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Students'    


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='teacher')
    position=models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='teacher_position',null=True)
    about_teacher=RichTextField(null=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Teachers' 

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_of_lesson',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Lessons' 

class Staff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='staff')
    position_choices=[
        ('director','Director'),
        ('asistant-director','Asistant')       
    ]
    position=models.CharField(max_length=50,choices=position_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    class Meta:
        verbose_name_plural = 'Staff' 

