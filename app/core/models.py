from django.db import models

# Create your models here.

class ClassName(models.Model):
    name=models.CharField(max_length=10)
    maximum_student=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField("staff.Student",related_name='student_of_class')
    lessons=models.ManyToManyField("staff.Lesson",related_name='lesson_of_class')
    teachers=models.ManyToManyField("staff.Teacher",related_name='teacher_of_class')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = ('Class')

class Notification(models.Model):
    message=models.CharField(max_length=255)
    user=models.ForeignKey('baseuser.User',on_delete=models.CASCADE ,related_name='received_user')
    time=models.DateTimeField(auto_now_add=True)

    
