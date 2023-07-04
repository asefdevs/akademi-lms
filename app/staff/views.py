from django.shortcuts import render, redirect,HttpResponse
from baseuser.forms import UserUpdateForm
from baseuser.decorators import student_required,teacher_required,superadmin_required,custom_login_required
from staff.models import Lesson, Student,Teacher
from .forms import EditStudentForm

@custom_login_required
@superadmin_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'edit-profile.html', context)

@custom_login_required
@superadmin_required
def student_list(request):
    form = EditStudentForm()
    context = {
        'students': Student.objects.all(),
    }
    return render(request, 'student.html', context)


@custom_login_required
@superadmin_required
def student_edit(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')  

        student = Student.objects.get(user_id=student_id)  
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')  
    else:
        form = EditStudentForm()
    return render(request, 'student-edit.html', {'students': students, 'form': form})


@custom_login_required
@student_required
def student_detail(request,student_id):
        context={
            'page_title': 'Student Detail',
            'student':Student.objects.get(user_id=student_id),
            'lesson':Lesson.objects.all(),
        
        }
        return render(request, 'student-detail.html', context)


@custom_login_required
@teacher_required
def teacher_detail(request,teacher_id):
     context={
          'lesson':Lesson.objects.all(),
          'page_title': 'Teacher Detail',
          'teacher':Teacher.objects.get(user_id=teacher_id)

     }
     return render(request,'teacher-detail.html',context)

@custom_login_required
@superadmin_required
def teacher_list(request):
    context={
        'teachers':Teacher.objects.all(),
    }
    return render(request,'teacher.html',context)

def error_404(request):
    return render(request,'page-error-404.html')

