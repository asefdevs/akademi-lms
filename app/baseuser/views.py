from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate

from . forms import RegisterForm,LoginForm
from staff.models import Student,Teacher
from .decorators import unauthorized_user,superadmin_required

# Create your views here.
# @superadmin_required
def register_page (request):
    context={
        'form': RegisterForm(),
    }
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.user_type == 'student':
                 student=Student.objects.create(user=user)
                 student.save()
            elif user.user_type == 'teacher':
                 teacher=Teacher.objects.create(user=user)
                 teacher.save()
            return redirect('login')
        
    return render(request, 'page-register.html',context)

@unauthorized_user
def login_page(request):
    context = {'form': LoginForm()}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Invalid credentials'
    
    return render(request, 'page-login.html', context) 


def logout_user(request):
    logout(request)
    return redirect('login')



