from django.urls import path
from . import views

urlpatterns = [
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('student_detail/',views.student_detail,name='student'),
    path('error_404/',views.error_404,name='error_permission'),
    path('teacher_detail/',views.teacher_detail,name='teacher'),
    
]