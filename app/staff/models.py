from django.db import models
from baseuser.models import User
from ckeditor.fields import RichTextField


class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_user')
    lesson = models.ManyToManyField('Lessons', related_name='students',blank=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Students' 

class Lessons(models.Model):
    title=models.CharField(max_length=50)
    season=models.ForeignKey('core.Seasons',on_delete=models.CASCADE,related_name='season_of_lesson')
    section=models.ManyToManyField('Sections',related_name='section_of_lesson',blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Lessons' 

class Sections(models.Model):
    title=models.CharField(max_length=50)
    teacher=models.ForeignKey('Teachers', on_delete=models.SET_NULL,related_name='teacher_of_seasonLesson',null=True)
    students=models.ManyToManyField('Students', blank=True,related_name='students_of_section')
    max_student_count=models.IntegerField(null=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Sections' 
class Teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='teacher')
    position=models.CharField(max_length=250)
    about_teacher=models.TextField(null=True , blank=True)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Teachers' 


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

