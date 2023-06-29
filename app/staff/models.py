# from django.db import models
# from baseuser.models import User
# # Create your models here.

# class Base(models.Model):
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     class Meta:
#         abstract=True

    
# class Student(Base):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     city=models.CharField(max_length=300)
#     number=models.CharField(max_length=50)
#     grade=models.CharField(max_length=200)

#     def __str__(self):
#         return self.first_name
#     class Meta:
#         verbose_name_plural=('Students')


