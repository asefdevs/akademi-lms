from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add_class/',views.add_class,name='add_class'),
]