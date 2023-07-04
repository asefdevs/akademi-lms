from django.urls import path
from . import views

urlpatterns = [
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('student_detail/<int:student_id>/',views.student_detail,name='student_detail'),
    path('error_404/',views.error_404,name='error_permission'),
    path('teacher_detail/<int:teacher_id>/',views.teacher_detail,name='teacher_detail'),
    path('students/',views.student_list,name='students'),  
    path('student-edit/',views.student_edit,name='student-edit'),
    path('teachers/',views.teacher_list,name='teachers'),


    
]