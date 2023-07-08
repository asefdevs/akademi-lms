from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from . forms import RegisterForm,LoginForm
from staff.models import Staff, Student,Teacher
from .decorators import unauthorized_user,superadmin_required,custom_login_required
from django.contrib import messages

# Create your views here.
@custom_login_required
@superadmin_required
def register_teacher (request):
    context={
        'form': RegisterForm(),
        'page_title': 'Teacher Registration',
    }
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.user_type == 'teacher': 
                about_teacher=form.cleaned_data['about_teacher']
                teacher=Teacher.objects.create(user=user)
                teacher.about_teacher=about_teacher
                teacher.save()
                return redirect('teachers')
        else:
            form=RegisterForm(request.POST,request.FILES)
            messages.error(request,"Invalid credintials in form")

    return render(request, 'add-teacher.html',context)

@custom_login_required
@superadmin_required
def register_student(request):
    context={
        'form': RegisterForm(),
        'page_title':'Student Registration',
    }
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.user_type == 'student':
                grade=form.cleaned_data['grade']
                student=Student.objects.create(user=user)
                student.grade=grade
                student.save()
                return redirect('students')
        else:
            form=RegisterForm(request.POST,request.FILES)
            messages.error(request,"Invalid credintials in form")
    return render(request, 'add-student.html',context)


@custom_login_required
@superadmin_required
def register_staff(request):
    context={
        'form': RegisterForm(),
        'page_title': 'Register Staff',
    }
    if request.method == 'POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.user_type == 'admin':
                position=form.cleaned_data['position_staff'] 
                staff=Staff.objects.create(user=user)
                staff.position=position
                staff.save()
                return redirect('staff')
        else:
            form=RegisterForm(request.POST,request.FILES)

            messages.error(request,"Invalid credintials in form")

    return render(request, 'add-staff.html',context)
   
@unauthorized_user
def login_page(request):
    context={
        'form':LoginForm()
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")           
    return render(request, 'page-login.html',context)


def logout_user(request):
    logout(request)
    return redirect('login')



