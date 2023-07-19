from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('classes/',views.class_list,name='classes'),
    path('add_class/',views.add_class,name='add_class'),
    path('edit_class/<str:class_name>/',views.edit_class,name='edit-class'),
]