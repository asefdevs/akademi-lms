from django.contrib import admin
from staff.models import Student,Teacher,Lesson


# class Student_admin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             "fields": (
#                 'city','number','grade',
            
#             ),
#         }),
#     )
    
# admin.site.register(Student,Student_admin)

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Lesson)

