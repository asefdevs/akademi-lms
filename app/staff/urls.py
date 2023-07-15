from django.urls import path
from . import views

urlpatterns = [
    path('show_profile/',views.show_profile,name='show_profile'),  

    path('students/',views.student_list,name='students'),  
    path('student_detail/<int:student_id>/',views.student_detail,name='student_detail'),
    # path('edit_student/<int:student_id>/',views.student_edit,name='edit_student'),
    path('delete-student/', views.delete_student, name='delete_student'),
    path('teachers/',views.teacher_list,name='teachers'),
    path('teacher_detail/<int:teacher_id>/',views.teacher_detail,name='teacher_detail'),
    path('teacher_edit/<int:teacher_id>/',views.teacher_edit,name='teacher_edit'),
    path('delete-teacher/', views.delete_teacher, name='delete_teacher'),
    path('staff/',views.staff_list,name='staff'),  

    path('error_404/',views.error_404,name='error_permission'),


    
]