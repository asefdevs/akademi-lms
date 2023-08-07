from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('classes/',views.class_list,name='classes'),
    path('add_class/',views.add_class,name='add_class'),
    path('edit_class/<str:class_name>/',views.edit_class,name='edit-class'),
    path('add_lesson/',views.add_lesson,name='add-lesson'),
    path('lessons/', views.lesson_list, name='lessons'),
    path('lesson_detail/<int:lesson_id>/',views.lesson_detail,name='lesson-detail'),
    path('edit_lesson/<int:lesson_id>/', views.edit_lesson,name='edit-lesson'),
    path('edit_section/<int:section_id>/',views.edit_section,name='edit-section'),
    path('assignment_submit/<int:id>/',views.assignment_submit,name='assignment-submit'),
    path('edit_assignment/<int:id>/',views.edit_assignment,name='edit-assignment'),



]