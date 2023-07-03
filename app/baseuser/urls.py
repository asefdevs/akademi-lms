from django.urls import path
from . import views

urlpatterns = [

    path('register_teacher/',views.register_teacher,name='register-teacher'),
    path('register_student/',views.register_student,name='register-student'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),

]