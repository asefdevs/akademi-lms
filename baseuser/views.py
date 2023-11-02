from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from . forms import RegisterForm,LoginForm
from staff.models import Staff, Students,Teachers,Lessons
from .decorators import unauthorized_user,superadmin_required,custom_login_required
from django.contrib import messages
from core.models import Classes,Notification


# Create your views here.
@custom_login_required
@superadmin_required
def register_teacher(request):
    context = {
        'form': RegisterForm(initial={'user_type': 'teacher'}),
        'page_title': 'Teacher Registration',
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            if user.user_type == 'teacher':
                about_teacher = form.cleaned_data['about_teacher']
                position_teacher = form.cleaned_data['position_teacher']  
                teacher = Teachers.objects.create(user=user, about_teacher=about_teacher, position=position_teacher)
                teacher.save()
                # lessons=Lesson.objects.get(title=position_teacher)
                # lessons.teacher.add(teacher)
                return redirect('teachers')
        else:
            print(form.errors)
            # form = RegisterForm()
            context['form']=form


    return render(request, 'add-teacher.html', context)


@custom_login_required
@superadmin_required
def register_student(request):
    context={
        'form': RegisterForm(initial={'user_type': 'student'}),
        'page_title':'Student Registration',
    }
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.user_type == 'student':
                student=Students.objects.create(user=user)
                student.save()
                classname=form.cleaned_data['classname']
                class_info=Classes.objects.get(name=classname)
                class_info.student.add(student)
                message=f'You are added to the class : {class_info.name} '
                notification=Notification.objects.create(message=message,user=user)
                notification.save()
                return redirect('students')
        else:
            print(form.errors)
            context['form']=form
   

    return render(request, 'add-student.html',context)


@custom_login_required
@superadmin_required
def register_staff(request):
    context = {
        'form': RegisterForm(initial={'user_type':'admin'}),
        'page_title': 'Register Staff',
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            if user.user_type == 'admin':
                position = form.cleaned_data['position_staff']
                staff = Staff.objects.create(user=user, position=position)
                staff.save()
                return redirect('staff')
        else:
            print(form.errors)
            context['form']=form


    return render(request, 'add-staff.html', context)
   
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



