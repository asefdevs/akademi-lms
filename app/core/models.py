from django.db import models

# Create your models here.

class Classes(models.Model):
    name=models.CharField(max_length=255,null=True)
    student=models.ManyToManyField('staff.Students',related_name='class_of_students',blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Classes'

class Seasons(models.Model):
    season_name=models.CharField(max_length=50)
    def __str__(self):
        return self.season_name
    class Meta:
        verbose_name_plural = 'Seasons'

 
class Settings(models.Model):
    active_season = models.ForeignKey('Seasons', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.active_season.season_name 

    class Meta:
        verbose_name_plural = 'Settings'


class Notification(models.Model):
    message=models.CharField(max_length=255)
    user=models.ForeignKey('baseuser.User',on_delete=models.CASCADE ,related_name='received_user')
    time=models.DateTimeField(auto_now_add=True)

    
