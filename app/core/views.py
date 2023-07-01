from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from baseuser.models import User
from staff.models import Student


# Create your views here.
@login_required
def home(request):
    context={
        'user_details': User.objects.all(),
    }
    return render(request,'index.html',context)

def student_list(request):
    context={
        'students': Student.objects.all(),

    }
    return render(request,'student.html',context)
