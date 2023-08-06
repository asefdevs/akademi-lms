from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone



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

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Notifications'
    
class Assignment(models.Model):
    title=models.CharField(max_length=250)
    lesson=models.ForeignKey('staff.Lessons',related_name='lesson_of_assignment',on_delete=models.CASCADE ,blank=True, null=True)
    description=RichTextField(blank=True)
    sender=models.ForeignKey('baseuser.User',on_delete=models.SET_NULL,blank=True,null=True,related_name='assigment_creator')
    receiver=models.ManyToManyField('staff.Sections', blank=True,related_name='assignment_receivers')
    is_active=models.BooleanField(default=True)
    max_try=models.IntegerField(default=3)
    created_at=models.DateTimeField(auto_now_add=True)
    deadline=models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Assigments'

class StudentsAssignment(models.Model):
    assignment=models.ForeignKey(Assignment, related_name='assigment',on_delete=models.CASCADE)
    user=models.ForeignKey('staff.Students',on_delete=models.CASCADE, blank=True,related_name='student_assigment'),
    comment=RichTextField(blank=True,null=True)
    file=models.FileField( upload_to='students_assigments',null=True, blank=True)
    def __str__(self):
        return self.assignment.title

    class Meta:
        verbose_name_plural = 'Students Assignment'




# from django.db import models
# from django.utils import timezone

# class Assignment(models.Model):
#     title = models.CharField(max_length=100)
#     receivers = models.CharField(max_length=100)
#     max_try_count = models.PositiveIntegerField(default=3)
#     is_active = models.BooleanField(default=True)
#     deadline = models.DateTimeField()

#     def tries_left_for_student(self, student):
#         # Assuming you have a related_name in AssignmentForStudents model for the foreign key.
#         assignment_for_student = self.assignment_for_students.filter(student=student).first()
#         if assignment_for_student:
#             return max(0, self.max_try_count - assignment_for_student.try_count)
#         return self.max_try_count

# class AssignmentForStudents(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_for_students')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Replace 'Student' with your actual student model.
#     try_count = models.PositiveIntegerField(default=0)

# class AssignmentForm(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Replace 'Student' with your actual student model.
#     file = models.FileField(upload_to='assignments/')
#     comments = models.TextField()

#     def save(self, *args, **kwargs):
#         # Check if the assignment is active and the deadline has not passed.
#         if not self.assignment.is_active:
#             raise ValueError("The assignment is not active.")
#         if self.assignment.deadline < timezone.now():
#             raise ValueError("The deadline has passed. You cannot submit the assignment.")
        
#         # Check the number of tries left for the student.
#         tries_left = self.assignment.tries_left_for_student(self.student)
#         if tries_left <= 0:
#             raise ValueError("You don't have any other try chances.")

#         # Update the try count for the student.
#         assignment_for_student = AssignmentForStudents.objects.filter(assignment=self.assignment, student=self.student).first()
#         if assignment_for_student:
#             assignment_for_student.try_count += 1
#             assignment_for_student.save()
#         else:
#             AssignmentForStudents.objects.create(assignment=self.assignment, student=self.student, try_count=1)

#         super().save(*args, **kwargs)
